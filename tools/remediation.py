import time
from typing import Dict, Any
from google.adk.tools import FunctionTool, ToolContext

def restart_banking_service(service_name: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Restarts a critical banking service to clear connection pools or stuck threads.
    
    Args:
        service_name (str): The name of the service (e.g., 'Mobile Gateway', 'Oracle Listener').
    """
    print(f"\n[Tool: Remediation] ⚠️  ATTEMPTING TO RESTART: {service_name}")
    print(f"[Tool: Remediation] ⏳ stopping service...")
    time.sleep(2)
    print(f"[Tool: Remediation] ⏳ starting service...")
    time.sleep(2)
    
    print(f"[Tool: Remediation] ✅ Service '{service_name}' is BACK ONLINE.")
    
    # Update the ticket state to RESOLVED
    tool_context.state['resolution_status'] = "SUCCESS"
    tool_context.state['status'] = "RESOLVED"
    
    return {"status": "SUCCESS", "message": f"{service_name} restarted successfully. Connection pool flushed."}

# CRITICAL: This enables the "Human-in-the-Loop" guardrail.
# The agent CANNOT execute this tool without user approval in the terminal.
remediation_tool = FunctionTool(func=restart_banking_service, require_confirmation=True)