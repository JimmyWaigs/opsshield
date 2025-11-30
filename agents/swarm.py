from google.adk.agents import LlmAgent, ParallelAgent
from tools import log_tool, db_tool, infra_tool

# --- Specialist 1: The Log Analyst ---
log_analyst = LlmAgent(
    model="gemini-2.0-flash",
    name="log_analyst",
    instruction="""
    You are a Senior Log Analyst. 
    1. Call `fetch_application_logs` to get the error trace.
    2. Summarize the specific error codes found.
    3. Output your findings clearly.
    """,
    tools=[log_tool]
)

# --- Specialist 2: The Database Expert ---
db_specialist = LlmAgent(
    model="gemini-2.0-flash",
    name="db_specialist",
    instruction="""
    You are an Oracle DBA.
    1. Call `check_db_locks` to analyze the database health.
    2. If you see connection pool exhaustion or locks, identify the blocking session.
    """,
    tools=[db_tool]
)

# --- Specialist 3: The Infra Engineer ---
infra_specialist = LlmAgent(
    model="gemini-2.0-flash",
    name="infra_specialist",
    instruction="""
    You are a Linux Systems Administrator.
    1. Call `check_server_health`.
    2. Rule out hardware resource exhaustion (CPU/RAM).
    """,
    tools=[infra_tool]
)

# --- Tier 2 Orchestrator: The Swarm ---
investigation_swarm = ParallelAgent(
    name="tier2_investigation_swarm",
    sub_agents=[log_analyst, db_specialist, infra_specialist]
)