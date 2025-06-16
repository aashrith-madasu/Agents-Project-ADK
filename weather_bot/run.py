import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agent import weather_agent, weather_agent_team


# @title Define Agent Interaction Function
async def call_agent_async(
    query: str, 
    runner: Runner, 
    user_id: str, 
    session_id: str
) -> str:
    """Sends a query to the agent and prints the final response."""

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found
    
    return final_response_text
    
        

async def run_team_conversation():
    
    print("\n--- Testing Agent Team Delegation ---")
    session_service = InMemorySessionService()
    APP_NAME = "weather_tutorial_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"
    session = session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    runner = Runner( # Or use InMemoryRunner
        agent=weather_agent_team ,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent '{weather_agent_team.name}'.")

    while True:
        user_query = input(f"\n>>> User Query: ")
        
        response_text = await call_agent_async(user_query,
                                               runner=runner,
                                               user_id=USER_ID,
                                               session_id=SESSION_ID)
        
        print(f"<<< Agent Response: {response_text}")
        


if __name__ == "__main__":
    try:
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
