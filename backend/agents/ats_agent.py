import os
from google.adk.agents import LlmAgent

ats_agent = LlmAgent(
    name="ats_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash-lite"),
    output_key="ats_tips",
    instruction="""You are an ATS (Applicant Tracking System) optimization expert.

You have the following data:

CV Data:
{cv_data}

Job Description Data:
{jd_data}

Analyze the CV against the job description and return ONLY a valid JSON object with no extra text:

{{
  "tips": [
    "Actionable tip 1",
    "Actionable tip 2",
    "Actionable tip 3",
    "Actionable tip 4",
    "Actionable tip 5"
  ],
}}

Provide 5-8 actionable tips. Focus on concrete changes the candidate can make.
Return only the JSON. No markdown, no explanation.""",
)
