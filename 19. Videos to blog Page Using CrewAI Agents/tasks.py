from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer


# Create a task for the agent
research_task = Task(
    description="""
    Identify the video {topic}. 
    
    Provide a comprehensive information about the video from the channel.
    """,
    expected_output="A comprehensive 3 paragraphs long report based on the {topic} of the video content.",
    agent=blog_researcher,
    tools=[yt_tool]
)

# writing task with language model configuration
write_task = Task(
    description="""
    get the info from the youtube channel on the topic {topic}. 
    """,
    expected_output="Summarize the info from the channel video on the topic {topic} and create the content for the blog.",
    agent=blog_writer,
    tools=[yt_tool],
    async_execution=False,
    output_file="new-blog-post-md"
)