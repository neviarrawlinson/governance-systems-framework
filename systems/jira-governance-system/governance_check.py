# Governance Validation Script (Interactive Version)

required_fields = [
    "implementation_plan",
    "validation_plan",
    "qa_plan",
    "monitoring_plan",
    "rollback_plan",
    "risk_assessment"
]

def get_user_input():
    change = {}

    print("\n--- Enter Change Request Details ---")

    for field in required_fields:
        value = input(f"Do you have {field}? (yes/no): ").strip().lower()
        if value == "yes":
            change[field] = True

    return change

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

# Run the program
change_request = get_user_input()
validate_change(change_request)