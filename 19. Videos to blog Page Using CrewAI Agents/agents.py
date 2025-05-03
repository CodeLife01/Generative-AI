from crewai import Agent
from tools import yt_tool
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4-0125-preview"

## Create a senior blog content researcher

blog_researcher = Agent(
    role="Blog Research From youtube Videos",
    goal= "get the relevant video content for the topic{topic} from Yt channel",
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding vidoes in AI Data Science, Machine Learning And Gen AI and make suggestion"
    ),
    tools=[yt_tool],
    allow_delegation=True,
    
)

## creating a senior blog writer Agent with YT tool

blog_writer = Agent(
    role="Blog Write",
    goal= "Narrate compelling tech stories about video{topic} from YT channel",
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bring new"
        "discoveries to light in an accessible manner"
    ),
    tools=[yt_tool],
    allow_delegation=False,
    
)