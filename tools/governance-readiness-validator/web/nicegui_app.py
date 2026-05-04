import os
import datetime
import json
from pathlib import Path

from nicegui import ui
from ai.ai_reviewer import review_change_with_ai

ui.page_title("Governance Readiness Validator")

report_text_global = ""


def generate_recommendations(missing, decision, risk_level):
    recommendations = []

    if "Rollback Plan" in missing:
        recommendations.append("Rollback plan is required, especially for production changes.")

    if "Implementation Plan" in missing:
        recommendations.append("Implementation plan should include step-by-step deployment details.")

    if "Risk Assessment" in missing:
        recommendations.append("Risk assessment is required to evaluate potential impact.")

    if "Manager Approval" in missing:
        recommendations.append("Manager approval must be completed before CAB review.")

    if "QA Plan" in missing:
        recommendations.append("QA plan should identify testing completed and the validator responsible.")

    if "Monitoring Plan" in missing:
        recommendations.append("Monitoring plan should explain how post-deployment health will be confirmed.")

    if risk_level == "High":
        recommendations.append("High-risk change. Add additional validation and stakeholder review before approval.")

    if decision == "Not Ready":
        recommendations.append("Change request should not proceed to CAB until critical gaps are resolved.")

    if decision == "Conditional":
        recommendations.append("Change may proceed only after listed gaps or required reviews are completed.")

    return recommendations


def generate_report_text(change_id, title, decision, score, risk, missing, recommendations, ai_review):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# Governance Readiness Report

## Metadata
- Generated: {timestamp}
- Change ID: {change_id}
- Title: {title}

## Results
- Decision: {decision}
- Score: {score}%
- Risk Level: {risk}

## Missing Requirements
"""

    if missing:
        for item in missing:
            report += f"- {item}\n"
    else:
        report += "- None\n"

    report += "\n## Recommendations\n"

    if recommendations:
        for rec in recommendations:
            report += f"- {rec}\n"
    else:
        report += "- None\n"

    report += f"""

## AI Governance Review

{ai_review if ai_review else "AI review was not generated."}
"""

    return report


def download_report():
    if report_text_global:
        ui.download(content=report_text_global, filename="governance_report.md")
    else:
        ui.notify("Run validation first", type="warning")


with ui.column().classes("w-full items-center p-6"):
    ui.label("Governance Readiness Validator").classes("text-3xl font-bold")
    ui.label(
        "AI-assisted GRC engineering tool for CAB readiness, risk review, and audit-ready outputs."
    ).classes("text-lg text-gray-600")

    with ui.card().classes("w-full max-w-4xl p-6 mt-6"):
        ui.label("Change Request Intake").classes("text-xl font-semibold")

        change_id = ui.input("Change ID", placeholder="CHG-001").classes("w-full")
        title = ui.input("Change Title", placeholder="Production deployment").classes("w-full")

        change_description = ui.textarea(
            "Change Description",
            placeholder="Describe the change in detail..."
        ).classes("w-full")

        environment = ui.select(
            ["Production", "Staging", "Corporate", "Development"],
            value="Production",
            label="Environment"
        ).classes("w-full")

        change_type = ui.select(
            ["Normal", "Standard", "Emergency", "Informational"],
            value="Normal",
            label="Change Type"
        ).classes("w-full")

        ui.label("Governance Requirements").classes("mt-4 font-semibold")

        implementation_plan = ui.checkbox("Implementation Plan Complete")
        validation_plan = ui.checkbox("Validation Plan Complete")
        qa_plan = ui.checkbox("QA Plan Complete")
        monitoring_plan = ui.checkbox("Monitoring Plan Complete")
        rollback_plan = ui.checkbox("Rollback Plan Complete")
        risk_assessment = ui.checkbox("Risk Assessment Complete")
        manager_approval = ui.checkbox("Manager Approval Complete")

        def load_sample_jira_ticket():
            sample_path = Path("sample_inputs/jira_ticket_sample.json")

            with open(sample_path, "r") as file:
                ticket = json.load(file)

            fields = ticket["fields"]

            change_id.value = ticket.get("key", "")
            title.value = ticket.get("summary", "")
            change_description.value = ticket.get("summary", "")
            environment.value = fields.get("environment", "Production")
            change_type.value = fields.get("change_type", "Normal")

            implementation_plan.value = bool(fields.get("implementation_plan"))
            validation_plan.value = bool(fields.get("validation_plan"))
            qa_plan.value = bool(fields.get("qa_plan"))
            monitoring_plan.value = bool(fields.get("monitoring_plan"))
            rollback_plan.value = bool(fields.get("rollback_plan"))
            risk_assessment.value = bool(fields.get("risk_assessment"))
            manager_approval.value = bool(fields.get("manager_approval"))

            ui.notify("Sample Jira ticket loaded", type="positive")

        ui.button("Load Sample Jira Ticket", on_click=load_sample_jira_ticket).classes("mt-4")

    with ui.card().classes("w-full max-w-4xl p-6 mt-4"):
        ui.label("Validation Results").classes("text-xl font-semibold")

        score_bar = ui.linear_progress(value=0).classes("w-full mt-2")
        score_label = ui.label("CAB Readiness Score: Not calculated").classes("text-lg")

        decision_label = ui.label("Decision: Not calculated").classes("text-lg font-bold")
        risk_label = ui.label("Risk Level: Not calculated").classes("text-md")

        missing_container = ui.column().classes("mt-4")
        recommendation_container = ui.column().classes("mt-4")
        ai_output_container = ui.column().classes("mt-4")

    def run_validation():
        global report_text_global

        required = {
            "Implementation Plan": implementation_plan.value,
            "Validation Plan": validation_plan.value,
            "QA Plan": qa_plan.value,
            "Monitoring Plan": monitoring_plan.value,
            "Rollback Plan": rollback_plan.value,
            "Risk Assessment": risk_assessment.value,
            "Manager Approval": manager_approval.value,
        }

        completed = sum(1 for value in required.values() if value)
        total = len(required)
        score = round((completed / total) * 100)

        missing = [name for name, value in required.items() if not value]

        risk_flags = 0
        if environment.value == "Production":
            risk_flags += 1
        if change_type.value == "Emergency":
            risk_flags += 1
        if score < 75:
            risk_flags += 1

        if risk_flags >= 2:
            risk_level = "High"
        elif risk_flags == 1:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        critical_missing = [
            name for name in ["Implementation Plan", "Rollback Plan", "Risk Assessment", "Manager Approval"]
            if name in missing
        ]

        if critical_missing:
            decision = "Not Ready"
        elif score >= 90:
            decision = "Ready"
        else:
            decision = "Conditional"

        score_bar.value = score / 100
        score_label.set_text(f"CAB Readiness Score: {score}%")

        decision_colors = {
            "Ready": "green",
            "Conditional": "orange",
            "Not Ready": "red",
        }

        decision_label.set_text(f"Decision: {decision}")
        decision_label.style(f"color: {decision_colors[decision]}")

        risk_label.set_text(f"Risk Level: {risk_level}")

        missing_container.clear()
        with missing_container:
            if missing:
                ui.label("Missing Requirements:").classes("font-semibold")
                for item in missing:
                    ui.label(f"- {item}")
            else:
                ui.label("Missing Requirements: None").classes("font-semibold")

        recommendations = generate_recommendations(missing, decision, risk_level)

        recommendation_container.clear()
        with recommendation_container:
            if recommendations:
                ui.label("Recommendations:").classes("font-semibold")
                for rec in recommendations:
                    ui.label(f"- {rec}")
            else:
                ui.label("Recommendations: No additional actions required.").classes("font-semibold")

        ai_output_container.clear()

        ai_review = review_change_with_ai(
            change_description.value,
            environment.value,
            change_type.value,
            missing,
            risk_level
        )

        with ai_output_container:
            ui.label("AI Governance Review").classes("font-semibold")
            ui.markdown(ai_review)

        report_text_global = generate_report_text(
            change_id.value,
            title.value,
            decision,
            score,
            risk_level,
            missing,
            recommendations,
            ai_review
        )

    ui.button("Run Governance Validation", on_click=run_validation).classes("mt-4")
    ui.button("Download Report", on_click=download_report).classes("mt-2")

ui.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080))
)