from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.multi_agent_langchain.tools.tools import web_search, scrape_url

load_dotenv()

llm = init_chat_model(
    "gemini-3.1-flash-lite",
    model_provider="google_genai",
    thinking_budget=0,
)

# Researcher Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a research assistant.

        Instructions:
        - Use web_search for questions requiring current or external information.
        - Carefully analyze the search results.
        - Never assume search results are accurate without checking them.
        - If information is unavailable, say so.
        - Never invent facts.
        """
    )

# Reader Agent
def build_reader_agent():
    return create_agent(
    model=llm,
    tools=[scrape_url],
)

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an expert research writer.
    Create detailed, factual and professional research reports.
    Do not invent facts or sources.
    """),
    ("human", """
    Write a research report on the following topic:

    Topic: {topic}

    Research:
    {research}

    Structure:
    1. Introduction
    2. Key Findings
    3. Conclusion
    4. Sources
    """),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """
    Review the research report below and evaluate it strictly.

    Report:
    {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ....
    - ....

    Areas to Improve:
    - ....
    - ....

    One line verdict:
    ....
    """),
])

critic_chain = critic_prompt | llm | StrOutputParser()