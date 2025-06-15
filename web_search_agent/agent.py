from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm

import os
from dotenv import load_dotenv
load_dotenv()

model = LiteLlm(
    model="openrouter/google/gemma-3-27b-it:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

root_agent = Agent(
    model=model,
    name='web_search_agent',
    description='Web search agent',
    instruction="""You are a helpful agent that can use the following tools:
    - google_search
    """,
    # instruction="You are a helpful agent that asks the user name first and then use their name to greet them.",
    tools=[google_search]
)
