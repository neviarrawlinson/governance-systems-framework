import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def review_change_with_ai(change_summary, environment, change_type, missing_items, risk_level):
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return """
AI Review Unavailable

OPENAI_API_KEY is not configured.

Fallback Review:
- Complete all required governance fields before CAB review.
- Validate rollback, monitoring, risk, and approval requirements.
- Generate the report after validation for audit traceability.
"""

        prompt = f"""
You are a senior GRC engineer reviewing a change request for CAB readiness.

Change Summary:
{change_summary}

Environment: {environment}
Change Type: {change_type}
Risk Level: {risk_level}

Missing Governance Items:
{missing_items}

Provide a concise governance review with:
1. Key risk concerns
2. Missing controls or evidence
3. Recommended remediation actions
4. CAB readiness recommendation

Keep the response professional, audit-focused, and practical.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    except Exception:
        return f"""
AI Review Fallback Mode

The AI service is currently unavailable, but the governance review can still proceed.

Summary:
- Risk Level: {risk_level}
- Change Type: {change_type}
- Environment: {environment}
- Missing Controls: {", ".join(missing_items) if missing_items else "None"}

Recommended Governance Actions:
- Resolve missing governance requirements before CAB approval.
- Confirm rollback, monitoring, validation, and approval evidence.
- Document decision rationale in the exported governance report.
- Escalate high-risk or production-impacting changes for additional review.
"""