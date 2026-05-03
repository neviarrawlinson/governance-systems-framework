import json
from pathlib import Path

REQUIRED_FIELDS = [
    "implementation_plan",
    "validation_plan",
    "qa_plan",
    "monitoring_plan",
    "rollback_plan",
    "risk_assessment",
    "business_justification",
    "deployment_window",
    "named_owner",
    "named_validator",
    "manager_approval"
]

CRITICAL_FIELDS = [
    "implementation_plan",
    "rollback_plan",
    "risk_assessment",
    "manager_approval"
]

def load_change_request(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def calculate_readiness_score(change):
    completed = sum(1 for field in REQUIRED_FIELDS if change.get(field) is True)
    total = len(REQUIRED_FIELDS)
    return round((completed / total) * 100)

def identify_missing_fields(change):
    return [field for field in REQUIRED_FIELDS if change.get(field) is not True]

def identify_critical_gaps(change):
    return [field for field in CRITICAL_FIELDS if change.get(field) is not True]

def determine_required_reviews(change):
    reviews = []

    if change.get("security_review_required") and not change.get("security_review_complete"):
        reviews.append("Security review is required but not complete.")

    if change.get("compliance_review_required") and not change.get("compliance_review_complete"):
        reviews.append("Compliance review is required but not complete.")

    return reviews

def determine_decision(score, missing_fields, critical_gaps, required_reviews):
    if critical_gaps:
        return "Not Ready"

    if required_reviews:
        return "Conditional"

    if score >= 90 and not missing_fields:
        return "Ready"

    if score >= 75:
        return "Conditional"

    return "Not Ready"

def determine_risk_level(change, score):
    risk_flags = 0

    if change.get("environment") == "Production":
        risk_flags += 1
    if change.get("customer_impact"):
        risk_flags += 1
    if change.get("compliance_impact"):
        risk_flags += 1
    if change.get("security_impact"):
        risk_flags += 1
    if score < 75:
        risk_flags += 1

    if risk_flags >= 4:
        return "High"
    if risk_flags >= 2:
        return "Medium"
    return "Low"

def generate_markdown_report(change, score, risk_level, decision, missing_fields, critical_gaps, required_reviews):
    report = f"""# Governance Readiness Report

## Change Summary

- Change ID: {change.get("change_id", "N/A")}
- Title: {change.get("title", "N/A")}
- Change Type: {change.get("change_type", "N/A")}
- Environment: {change.get("environment", "N/A")}

## Readiness Result

- CAB Readiness Score: {score}%
- Risk Level: {risk_level}
- Decision: {decision}

## Missing Requirements

{format_list(missing_fields)}

## Critical Gaps

{format_list(critical_gaps)}

## Required Review Actions

{format_list(required_reviews)}

## Recommended Next Action

{recommended_action(decision, critical_gaps, required_reviews)}
"""
    return report

def format_list(items):
    if not items:
        return "- None"
    return "\n".join([f"- {item}" for item in items])

def recommended_action(decision, critical_gaps, required_reviews):
    if decision == "Ready":
        return "Proceed to CAB review or implementation approval."

    if critical_gaps:
        return "Return the change request to the submitter and require critical governance fields before review."

    if required_reviews:
        return "Complete required Security and/or Compliance reviews before final approval."

    return "Resolve missing requirements before CAB review."

def main():
    input_file = Path("sample_inputs/sample_change.json")
    output_file = Path("outputs/change_readiness_report.md")

    change = load_change_request(input_file)

    score = calculate_readiness_score(change)
    missing_fields = identify_missing_fields(change)
    critical_gaps = identify_critical_gaps(change)
    required_reviews = determine_required_reviews(change)
    risk_level = determine_risk_level(change, score)
    decision = determine_decision(score, missing_fields, critical_gaps, required_reviews)

    report = generate_markdown_report(
        change,
        score,
        risk_level,
        decision,
        missing_fields,
        critical_gaps,
        required_reviews
    )

    output_file.write_text(report)

    print("\nGovernance Readiness Validation Complete")
    print(f"CAB Readiness Score: {score}%")
    print(f"Risk Level: {risk_level}")
    print(f"Decision: {decision}")
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    main()