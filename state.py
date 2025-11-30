from typing import TypedDict, Literal, Dict, List, Optional
import uuid

# Define valid status types for the incident
IncidentStatus = Literal["MONITORING", "INVESTIGATING", "PENDING_APPROVAL", "RESOLVED"]

class IncidentTicket(TypedDict):
    """
    The Shared Session State Schema.
    Acts as the 'Single Source of Truth' for all agents.
    """
    incident_id: str
    status: IncidentStatus
    
    # Tier 1 Output: The alert that triggered the workflow
    alert_details: Optional[str]
    
    # Tier 2 Outputs: Diagnostics from the Swarm
    logs_summary: Optional[str]      # From Log Analyst Agent
    db_health: Optional[Dict]        # From DB Specialist Agent
    infra_health: Optional[Dict]     # From Infra Specialist Agent
    
    # Tier 3 Outputs: Resolution Plan
    rca_report: Optional[str]        # Synthesized Root Cause Analysis
    proposed_fix: Optional[str]      # Action to be approved
    resolution_status: Optional[str] # Final outcome after fix

def get_initial_state() -> IncidentTicket:
    """Returns the blank ticket structure for a new session."""
    return {
        "incident_id": str(uuid.uuid4()),
        "status": "MONITORING",
        "alert_details": None,
        "logs_summary": None,
        "db_health": {},
        "infra_health": {},
        "rca_report": None,
        "proposed_fix": None,
        "resolution_status": None
    }