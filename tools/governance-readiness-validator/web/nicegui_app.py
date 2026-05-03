from nicegui import ui

ui.page_title("Governance Readiness Validator")

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


with ui.column().classes("w-full items-center p-6"):
    ui.label("Governance Readiness Validator").classes("text-3xl font-bold")
    ui.label(
        "AI-assisted GRC engineering tool for CAB readiness, risk review, and audit-ready outputs."
    ).classes("text-lg text-gray-600")

    with ui.card().classes("w-full max-w-4xl p-6 mt-6"):
        ui.label("Change Request Intake").classes("text-xl font-semibold")

        change_id = ui.input("Change ID", placeholder="CHG-001").classes("w-full")
        title = ui.input("Change Title", placeholder="Production deployment").classes("w-full")

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

    with ui.card().classes("w-full max-w-4xl p-6 mt-4"):
        ui.label("Validation Results").classes("text-xl font-semibold")

        score_bar = ui.linear_progress(value=0).classes("w-full mt-2")
        score_label = ui.label("CAB Readiness Score: Not calculated").classes("text-lg")

        decision_label = ui.label("Decision: Not calculated").classes("text-lg font-bold")
        risk_label = ui.label("Risk Level: Not calculated").classes("text-md")

        missing_container = ui.column().classes("mt-4")
        recommendation_container = ui.column().classes("mt-4")

    def run_validation():
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

    ui.button("Run Governance Validation", on_click=run_validation).classes("mt-4")

ui.run()