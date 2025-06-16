# @title Import necessary libraries
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support

from google.genai import types # For creating message Content/Parts
from dotenv import load_dotenv

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

from tools import (
    get_weather, say_hello, say_goodbye
)
print("Libraries imported.")

load_dotenv()
print("Loaded Env vars")


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


# @title Define Greeting and Farewell Sub-Agents

# If you want to use models other than Gemini, Ensure LiteLlm is imported and API keys are set (from Step 0/2)
# from google.adk.models.lite_llm import LiteLlm
# MODEL_GPT_4O, MODEL_CLAUDE_SONNET etc. should be defined
# Or else, continue to use: model = MODEL_GEMINI_2_0_FLASH

# --- Greeting Agent ---
greeting_agent = Agent(
    # Using a potentially different/cheaper model for a simple task
    model = AGENT_MODEL,
    # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                "Use the 'say_hello' tool to generate the greeting. "
                "If the user provides their name, make sure to pass it to the tool. "
                "Do not engage in any other conversation or tasks.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
    tools=[say_hello],
)
print(f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")


# --- Farewell Agent ---
farewell_agent = Agent(
    # Can use the same or a different model
    model = AGENT_MODEL,
    # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                "Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
    tools=[say_goodbye],
)
print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")



# @title Define the Root Agent with Sub-Agents

# Ensure sub-agents were created successfully before defining the root agent.
# Also ensure the original 'get_weather' tool is defined.
root_agent = None
runner_root = None # Initialize runner

# Let's use a capable Gemini model for the root agent to handle orchestration
root_agent_model = AGENT_MODEL

weather_agent_team = Agent(
    name="weather_agent_v2", # Give it a new version name
    model=root_agent_model,
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                "Intelligently convert any aliases of cities to one of the following : newyork, london, tokyo"
                "You have specialized sub-agents: "
                "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                "If it's a weather request, handle it yourself using 'get_weather'. "
                "For anything else, respond appropriately or state you cannot handle it.",
    tools=[get_weather], # Root agent still needs the weather tool for its core task
    # Key change: Link the sub-agents here!
    sub_agents=[greeting_agent, farewell_agent]
)
print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")