# @title Import necessary libraries
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support

from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore") # Ignore all warnings
import logging
logging.basicConfig(level=logging.ERROR)

from tools import (
    get_weather, say_hello, say_goodbye
)
from prompts import Prompts


# @title Define the Weather Agent
# Use one of the model constants defined earlier
AGENT_MODEL = 'gemini-2.0-flash' # Starting with Gemini

weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather], # Pass the function directly
)

print(f"Agent '{weather_agent.name}' created using model '{AGENT_MODEL}'.")


# --- Greeting Agent ---
greeting_agent = Agent(
    # Using a potentially different/cheaper model for a simple task
    model = AGENT_MODEL,
    name="greeting_agent",
    instruction=Prompts.greeting_agent,
    description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
    tools=[say_hello],
)
print(f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")


# --- Farewell Agent ---
farewell_agent = Agent(
    model=AGENT_MODEL,
    name="farewell_agent",
    instruction=Prompts.farewell_agent,
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
    tools=[say_goodbye],
)
print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")



weather_agent_team = Agent(
    name="weather_agent_v2", # Give it a new version name
    model=AGENT_MODEL,
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction=Prompts.weather_agent_team,
    tools=[get_weather], # Root agent still needs the weather tool for its core task
    # Key change: Link the sub-agents here!
    sub_agents=[greeting_agent, farewell_agent]
)
print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{AGENT_MODEL}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")