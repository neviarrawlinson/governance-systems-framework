# Governance Readiness Validator

The Governance Readiness Validator is a lightweight GRC engineering tool that evaluates whether a change request is ready for CAB approval.

It simulates real governance decision logic using structured inputs and produces a readiness score, risk level, decision, and audit-ready report.

---

## What It Does

This tool evaluates:

- Required governance fields
- Critical control gaps
- Security and compliance review requirements
- Risk indicators
- CAB readiness score

---

## Output

The tool produces:

- CAB Readiness Score (0–100%)
- Risk Level (Low / Medium / High)
- Decision (Ready / Conditional / Not Ready)
- Markdown report for audit and documentation

---

## How to Run

### Step 1: Navigate to the tool
cd tools/governance-readiness-validator

### Step 2: Run the validator
python governance_validator.py


---

## Input

Edit the sample input file:
sample_inputs/sample_change.json



You can simulate different change scenarios by updating values.

---

## Output Report

After running, a report is generated here:
outputs/change_readiness_report.md


---

## Example Use Cases

- Validate change requests before CAB
- Simulate governance enforcement logic
- Generate audit-ready documentation
- Demonstrate GRC engineering concepts

---

## Future Enhancements

- Interactive CLI input
- Web-based UI (Streamlit)
- Integration with Jira APIs
- Dashboard for governance metrics
- RCA linkage and tracking