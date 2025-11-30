import random
import time
from typing import Dict, Any
from google.adk.tools import FunctionTool, ToolContext

# --- Tool 1: Log Analysis (with Context Compaction) ---
def fetch_application_logs(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Fetches recent application logs. 
    Applies Context Compaction to remove noise and timestamps to fit in LLM context.
    """
    print("\n[Tool: LogAnalyst] 📜 Fetching and compacting logs...")
    time.sleep(1) # Simulate network lag

    # Simulated raw logs (Massive block of text)
    raw_logs = [
        "[2025-11-28 16:30:01] INFO: Health Check OK",
        "[2025-11-28 16:30:02] INFO: Transaction 9982 processed",
        "[2025-11-28 16:30:05] ERROR: ConnectionRefusedError: Oracle DB 10.0.0.5:1521",
        "[2025-11-28 16:30:05] CRITICAL: Connection Pool Exhausted (Max: 100)",
        "[2025-11-28 16:30:06] INFO: Retrying connection...",
    ]

    # Context Compaction Logic: Filter only ERRORS/CRITICAL to save tokens
    compacted_logs = [line for line in raw_logs if "ERROR" in line or "CRITICAL" in line]
    
    findings = "\n".join(compacted_logs)
    
    # Save to Shared Ticket
    tool_context.state['logs_summary'] = findings
    
    return {"status": "SUCCESS", "relevant_logs": findings}

# --- Tool 2: Database Diagnostics ---
def check_db_locks(tool_context: ToolContext) -> Dict[str, Any]:
    """Checks the Core Banking Database for locked sessions and pool usage."""
    print("\n[Tool: DBSpecialist] 🗄️  Querying Oracle DB performance views...")
    time.sleep(2) # Simulate query time

    # Simulate finding the root cause
    db_report = {
        "active_sessions": 102,
        "max_pool_size": 100,
        "wait_event": "enq: TX - row lock contention",
        "blocking_session_id": "SID_998"
    }

    # Save to Shared Ticket
    tool_context.state['db_health'] = db_report

    return {"status": "CRITICAL_LOAD", "details": db_report}

# --- Tool 3: Infrastructure Metrics ---
def check_server_health(tool_context: ToolContext) -> Dict[str, Any]:
    """Checks CPU, RAM, and Disk I/O."""
    print("\n[Tool: InfraSpecialist] 📉 Checking Gateway Server metrics...")
    time.sleep(1) 

    infra_report = {
        "cpu_usage": "12%", # Low CPU implies it's not a compute issue
        "memory_usage": "45%",
        "disk_io": "NORMAL"
    }

    # Save to Shared Ticket
    tool_context.state['infra_health'] = infra_report

    return {"status": "HEALTHY", "metrics": infra_report}

# Wrap as ADK Tools
log_tool = FunctionTool(func=fetch_application_logs)
db_tool = FunctionTool(func=check_db_locks)
infra_tool = FunctionTool(func=check_server_health)