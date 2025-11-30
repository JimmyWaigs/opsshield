import time
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import FunctionTool, ToolContext
from tools import health_tool

# --- Helper Tools for Flow Control ---

def trigger_escalation(tool_context: ToolContext) -> str:
    """
    Triggers the Tier 2 Investigation Swarm.
    Use this ONLY when the system health status is 'CRITICAL'.
    """
    print("\n[Watchdog] ⚠️  CRITICAL DETECTED. Escalating to Tier 2 Swarm...")
    
    # CRITICAL: This is the ADK mechanism to break out of a LoopAgent
    # When set to True, the loop stops immediately and returns control to the parent
    tool_context.actions.escalate = True
    
    return "Escalation signal sent. Loop terminating."

def wait_interval() -> str:
    """Waits for a short period to simulate a polling interval."""
    # We use 3 seconds for the demo so you don't have to wait long 
    # In production, this might be 30 or 60 seconds
    time.sleep(3) 
    return "Polling interval complete."

# Wrap helpers as ADK tools
escalate_tool = FunctionTool(func=trigger_escalation)
wait_tool = FunctionTool(func=wait_interval)

# --- Agent Definitions ---

# 1. The Decision Maker (LLM Agent)
# This agent analyzes the tool output and makes the decision to continue or stop
health_monitor = LlmAgent(
    model="gemini-2.0-flash",
    name="health_monitor",
    instruction="""
    You are the OpsShield Watchdog. Your sole responsibility is to monitor banking infrastructure.

    LOOP LOGIC:
    1. Call `check_banking_infrastructure`.
    2. Analyze the 'status' field in the result.
    
    DECISION TREE:
    - IF 'HEALTHY': 
        - Print a short confirmation (e.g., "System Green").
        - Call `wait_interval` to pause before the next check.
    - IF 'CRITICAL':
        - Do NOT wait.
        - Immediately call `trigger_escalation`.
    """,
    tools=[health_tool, escalate_tool, wait_tool]
)

# 2. The Looper (Workflow Agent)
# This keeps the health_monitor running indefinitely until 'escalate' is triggered
watchdog_agent = LoopAgent(
    name="tier1_watchdog_loop",
    sub_agents=[health_monitor],
    # We set a limit for safety during development, but in prod this could be higher
    max_iterations=20 
)