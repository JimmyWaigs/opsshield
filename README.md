# OpsShield: Autonomous L2 Incident Response System 🛡️

**Google AI Agents Intensive Capstone Project**

OpsShield is an enterprise-grade Multi-Agent System designed to automate Level 2 (L2) production support for banking infrastructure. It reduces Mean Time To Resolution (MTTR) by autonomously detecting, diagnosing, and remediating critical incidents with human-in-the-loop oversight.

## 🚩 Problem Statement
In the banking sector, L2 Application Support engineers face a critical challenge: **Mean Time To Resolution (MTTR)**. When a high-severity incident occurs (e.g., a mobile banking outage), valuable minutes are wasted manually gathering logs, querying databases, and checking server health. Engineers must context-switch between multiple monitoring tools to diagnose the root cause, delaying the fix and impacting customer trust. Traditional automation scripts are brittle and lack the reasoning capabilities to handle complex, multi-variable failures.


## 💡 Solution
OpsShield replaces the reactive "War Room" model with a proactive **Agentic Swarm**. Instead of waiting for a human to investigate, OpsShield continuously monitors infrastructure and autonomously spins up specialized AI experts to diagnose issues in parallel. It mimics the workflow of a Major Incident Team but operates at machine speed, ensuring that by the time a human is notified, the root cause has been identified and a fix is ready for approval.

## 🏗️ Architecture
The system utilizes a **Three-Tier Agent Architecture** powered by the Google Agent Development Kit (ADK).

### **Tier 1: The Watchdog (Loop Agent)**
* **Role:** The Sentry.
* **Function:** Runs an infinite monitoring loop executing a `check_system_health` tool.
* **Behavior:** Handles "Healthy" states silently. Instantly triggers an escalation to Tier 2 upon detecting a `CRITICAL` signal (e.g., API Latency > 2000ms).


### **Tier 2: The Investigation Swarm (Parallel Agent)**
* **Role:** The Analysts.
* **Function:** Spins up three specialist agents simultaneously to diagnose the root cause:
    1.  **Log Analyst:** Uses **Context Compaction** to filter noise from logs and identify error codes (e.g., `ConnectionRefused`).
    2.  **Database Specialist:** Queries internal views to identify locked sessions or connection pool exhaustion.
    3.  **Infra Engineer:** Checks CPU/RAM metrics to rule out hardware resource exhaustion.
* **Output:** Each agent writes structured findings to a shared "Incident Ticket" (Session State).

### **Tier 3: The Remediation Controller (Sequential Agent)**
* **Role:** The Incident Manager.
* **Function:** Synthesizes findings into a Root Cause Analysis (RCA) and selects a remediation plan.
* **Safety Guardrail:** Implements ADK's **Tool Confirmation** feature. The agent *cannot* execute the fix (e.g., restarting a service) without explicit human approval via the CLI.

## 🛠️ Tech Stack
* **Framework:** Google Agent Development Kit (ADK)
* **Model:** Gemini 2.0 Flash
* **State Management:** `InMemorySessionService` with a strict `TypedDict` schema for the shared Incident Ticket.
* **Observability:** Integrated **AgentOps** for execution tracing.
* **Tools:** Custom Python tools utilizing `ToolContext` for state manipulation and `FunctionTool` for guardrails.

## 🚦 Setup & Installation

### Prerequisites
* Python 3.9+
* A Google Cloud Project (optional) or Google AI Studio API Key

### Installation Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/JimmyWaigs/opsshield.git](https://github.com/JimmyWaigs/opsshield.git)
    cd opsshield
    ```

2.  **Set up Virtual Environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```ini
    GOOGLE_API_KEY="your-gemini-api-key"
    GOOGLE_GENAI_USE_VERTEXAI=False
    AGENTOPS_API_KEY="your-agentops-key" # Optional: For observability
    ```

## 🚀 Usage Guide
To run the full simulation, execute the main script:

```bash
python3 run.py