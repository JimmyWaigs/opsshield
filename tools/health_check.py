import random
from typing import Dict, Any
from google.adk.tools import FunctionTool, ToolContext

def check_banking_infrastructure(tool_context: ToolContext, simulate_failure: bool = False) -> Dict[str, Any]:
    """
    Performs a health check on critical banking components (Mobile API, ATM Switch, Core DB).
    
    Args:
        simulate_failure (bool): If True, forces a CRITICAL failure scenario for testing purposes.
                                 Defaults to False (simulates normal healthy operations).
    
    Returns:
        dict: A dictionary containing the overall status ('HEALTHY' or 'CRITICAL') and specific metrics.
    """
    
    print(f"\n[Tool] 🔍 Running System Health Check... (Simulation: {'FAILURE' if simulate_failure else 'NORMAL'})")

    # 1. Access the shared 'Incident Ticket' via ToolContext
    # This allows the tool to directly update the ticket if it finds an issue
    current_state = tool_context.state

    # 2. Simulate Metrics
    if simulate_failure:
        # Scenario: Database Connection Pool Exhaustion
        metrics = {
            "mobile_api_latency": "2500ms", # High latency
            "atm_switch_status": "UP",
            "core_db_connections": "98/100", # Dangerously high
            "error_rate": "15%"
        }
        status = "CRITICAL"
        alert_details = "CRITICAL ALERT: Mobile Banking API high latency. DB Connection pool at 98% capacity."
    else:
        # Healthy Scenario
        metrics = {
            "mobile_api_latency": f"{random.randint(20, 150)}ms",
            "atm_switch_status": "UP",
            "core_db_connections": f"{random.randint(10, 40)}/100",
            "error_rate": "0.01%"
        }
        status = "HEALTHY"
        alert_details = None

    # 3. Write Findings directly to the Shared State (The "Ticket")
    # This ensures that even if the agent context is lost, the incident data persists in the session.
    # We update the state delta which the Runner commits automatically[cite: 2138].
    tool_context.state['last_health_check'] = metrics
    
    if status == "CRITICAL":
        tool_context.state['status'] = "INVESTIGATING"
        tool_context.state['alert_details'] = alert_details
        print(f"[Tool] 🚨 CRITICAL FAILURE DETECTED! Updating Incident Ticket status to INVESTIGATING.")
    else:
        print(f"[Tool] ✅ System Healthy. Metrics: {metrics}")

    # 4. Return structured data for the LLM to reason about
    return {
        "status": status,
        "metrics": metrics,
        "timestamp": "2025-11-28 T16:35:00Z" # In a real app, use datetime.now()
    }

# Wrap the function as an ADK FunctionTool so the agent can use it
health_tool = FunctionTool(func=check_banking_infrastructure)