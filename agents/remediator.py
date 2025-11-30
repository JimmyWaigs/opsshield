from google.adk.agents import LlmAgent
from tools.remediation import remediation_tool

# This agent synthesizes the findings from Tier 2 and fixes the issue
remediation_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="remediation_controller",
    instruction="""
    You are the Major Incident Manager.
    
    YOUR INPUT:
    - You will see the 'logs_summary' and 'db_health' from the previous agents.
    
    YOUR JOB:
    1. Draft a Root Cause Analysis (RCA) based on the findings.
    2. Identify the failing service.
    3. Call `restart_banking_service` to fix it.
    
    NOTE: The tool will ask the human for confirmation. You must handle the response.
    """,
    tools=[remediation_tool]
)