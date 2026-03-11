from google.adk.agents import LlmAgent
""" this agent will be developed in future """
cover_letter_agent = LlmAgent(
    name="cover_letter_agent",
    model="gemini-2.5-flash",
    output_key="cover_letter",
    instruction="""You are a cover letter writing assistant.""",
)
