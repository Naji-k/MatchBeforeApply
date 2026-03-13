import os
from google.adk.agents import LlmAgent

""" this agent will be developed in future """
cover_letter_agent = LlmAgent(
    name="cover_letter_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash-lite"),
    output_key="cover_letter",
    instruction="""You are a cover letter writing assistant.""",
)
