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
    get_weather, say_hello, say_goodbye, get_weather_stateful
)
from utils import Prompts


AGENT_MODEL = 'gemini-2.0-flash' 

weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL, 
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather], 
)


# --- Greeting Agent ---
greeting_agent = Agent(
    name="greeting_agent",
    model = AGENT_MODEL,
    description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
    instruction=Prompts.greeting_agent,
    tools=[say_hello],
)


# --- Farewell Agent ---
farewell_agent = Agent(
    name="farewell_agent",
    model=AGENT_MODEL,
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
    instruction=Prompts.farewell_agent,
    tools=[say_goodbye],
)


weather_agent_team = Agent(
    name="weather_agent_v2",
    model=AGENT_MODEL,
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction=Prompts.weather_agent_team,
    tools=[get_weather_stateful],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_weather_report"
)