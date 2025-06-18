from vertexai.preview import reasoning_engines
from agent import weather_agent_team

app = reasoning_engines.AdkApp(
    agent=weather_agent_team,
    enable_tracing=True,
)