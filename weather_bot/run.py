import asyncio
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types

from .agent import root_agent


async def call_agent_async(
    query: str, 
    runner: Runner, 
    user_id: str, 
    session_id: str
) -> str:
    """Sends a query to the agent and prints the final response."""

    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                
            elif event.actions and event.actions.escalate: 
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                
            break 
    
    return final_response_text
    
        

async def run_team_conversation():
    
    session_service = InMemorySessionService()
    
    APP_NAME = "weather_tutorial_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"
    initial_state = {
        "user_preference_temperature_unit": "Celsius"
    }
    
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID,
        state=initial_state
    )
    
    if not session:
        raise Exception("Session not created")

    runner = Runner(
        agent=root_agent ,
        app_name=APP_NAME,
        session_service=session_service
    )

    while True:
        user_query = input(f"\n>>> User Query: ")
        
        response_text = await call_agent_async(user_query,
                                               runner=runner,
                                               user_id=USER_ID,
                                               session_id=SESSION_ID)
    
        print(f"<<< Agent Response: {response_text}")
        
        session = session_service.get_session(app_name=APP_NAME,
                                              user_id= USER_ID,
                                              session_id=SESSION_ID)
        
        print(f"Agent State: {session.state}")
        


if __name__ == "__main__":
    try:
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
