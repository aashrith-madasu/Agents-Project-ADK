import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agent import weather_agent


# @title Setup Session Service and Runner

# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001" # Using a fixed ID for simplicity

# # Create the specific session where the conversation will happen
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=weather_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)
print(f"Runner created for agent '{runner.agent.name}'.")



# @title Define Agent Interaction Function
 # For creating message Content/Parts

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
        print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

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
    
  
  
  
  
# @title Run the Initial Conversation

# We need an async function to await our interaction helper
async def run_conversation():
    
    while True:
        user_query = input(f"\n>>> User Query: ")
        
        response_text = await call_agent_async(user_query,
                               runner=runner,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        
        print(f"<<< Agent Response: {response_text}")
        
    # await call_agent_async("What is the weather like in London?",
    #                                    runner=runner,
    #                                    user_id=USER_ID,
    #                                    session_id=SESSION_ID)

    # await call_agent_async("How about Paris?",
    #                                    runner=runner,
    #                                    user_id=USER_ID,
    #                                    session_id=SESSION_ID) # Expecting the tool's error message

    # await call_agent_async("Tell me the weather in New York",
    #                                    runner=runner,
    #                                    user_id=USER_ID,
    #                                    session_id=SESSION_ID)

# Execute the conversation using await in an async context (like Colab/Jupyter)
# await run_conversation()

# --- OR ---

# Uncomment the following lines if running as a standard Python script (.py file):
if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")