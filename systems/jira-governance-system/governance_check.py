# Governance Validation Script

required_fields = [
    "implementation_plan",
    "validation_plan",
    "qa_plan",
    "monitoring_plan",
    "rollback_plan",
    "risk_assessment"
]

def validate_change(change):
    missing = [field for field in required_fields if field not in change]

    print("\n--- Governance Validation Result ---")

    if missing:
        print("❌ Change request is NOT ready for CAB")
        print("Missing fields:")
        for field in missing:
            print(f"- {field}")
    else:
        print("✅ Change request is CAB ready")

# Example change request (test case)
change_request = {
    "implementation_plan": "Defined",
    "validation_plan": "Defined",
    "qa_plan": "Defined"
}

validate_change(change_request)