import asyncio
import os
from dotenv import load_dotenv

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents import SequentialAgent
from google.genai import types 

from state import get_initial_state
# Import ALL tiers
from agents import watchdog_agent, investigation_swarm, remediation_agent

load_dotenv()

async def main():
    print("🛡️  OpsShield System Initializing...")

    session_service = InMemorySessionService()
    app_name = "opsshield_v1"
    user_id = "l2_operator"
    session_id = "incident_001"

    # Create Session
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id,
        state=get_initial_state() 
    )

    # --- THE MASTER WORKFLOW ---
    # We use a SequentialAgent to chain the tiers together.
    # 1. Watchdog (loops until critical)
    # 2. Swarm (diagnoses in parallel)
    # 3. Remediator (fixes with approval)
    master_workflow = SequentialAgent(
        name="opsshield_master_flow",
        sub_agents=[watchdog_agent, investigation_swarm, remediation_agent]
    )

    runner = Runner(
        agent=master_workflow, 
        app_name=app_name,
        session_service=session_service
    )

    print(f"🚀 Starting Autonomous L2 Support Workflow.")
    print(f"👉 Scenario: We will trigger a failure. You must APPROVE the fix when asked.")
    print("-" * 50)

    # Trigger the chaos immediately for the demo
    user_msg = types.Content(role="user", parts=[types.Part(text="Run a health check with failure simulation")])

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_msg
    ):
        # Print Agent Thoughts
        if event.content and event.content.parts:
            print(f"🤖 [{event.author}]: {event.content.parts[0].text}")
        
        # Handle the Human-in-the-Loop Confirmation Request
        # The ADK sends a specific function call when it needs approval
        for call in event.get_function_calls():
            if call.name == "adk_request_confirmation":
                print("\n" + "="*60)
                print("🛑 GUARDRAIL ACTIVATED: The agent wants to execute a critical action.")
                print(f"   Action: {call.args.get('name')}") # Name of the tool being called
                print("   Do you authorize this? (yes/no)")
                
                user_approval = input("   > ").strip().lower()
                
                # Send the approval/rejection back to the agent
                # We reuse the runner to send the special confirmation response
                approval_response = types.Content(
                    role="user",
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name="adk_request_confirmation",
                            id=call.id,
                            response={"confirmed": user_approval in ["yes", "y"]}
                        )
                    )]
                )
                
                # We inject the response immediately
                async for sub_event in runner.run_async(user_id=user_id, session_id=session_id, new_message=approval_response):
                     if sub_event.content and sub_event.content.parts:
                        print(f"🤖 [{sub_event.author}]: {sub_event.content.parts[0].text}")

    print("-" * 50)
    final_session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    print(f"📊 FINAL STATUS: {final_session.state['status']}")

if __name__ == "__main__":
    asyncio.run(main())