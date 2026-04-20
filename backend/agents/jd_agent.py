import os
from google.adk.agents import LlmAgent
from google.adk.tools import url_context
from pydantic import BaseModel
from typing import List


class JobDescription(BaseModel):
    job_title: str
    company: str
    required_skills: List[str]
    preferred_skills: List[str]
    nice_to_have: List[str]
    experience_required: str
    keywords: List[str]


jd_agent = LlmAgent(
    name="jd_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash-lite"),
    output_key="jd_data",
    tools=[url_context],
    instruction="""You are an expert Job Description analyst with years of recruiting experience.

The user message contains the job description to parse. It starts with "jd_type: url" or "jd_type: text" followed by the content.

- If jd_type is "url": call the url_context tool with the URL, then parse the fetched content.
- If jd_type is "text": parse the content directly.

PARSING RULES:
- required_skills: ONLY skills explicitly marked as required, must-have, or essential
- preferred_skills: skills marked as preferred, nice-to-have,
- nice_to_have: skills mentioned as optional or advantageous
- keywords: ATS-relevant terms that appear frequently or are emphasized in the JD
- experience_required: exact years if mentioned, otherwise infer from seniority
- If a skill appears ONLY in responsibilities section — put it in preferred_skills, not required_skills
- Ignore generic soft skills like "communication", "teamwork", "problem solving" — do not include them
- If JD has 10+ required skills it is likely bloated — use judgment to identify the truly critical ones

Extract and return ONLY a valid JSON object with no extra text:

{
  "job_title": "string",
  "company": "string",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill1", "skill2"],
  "nice_to_have": ["skill1", "skill2"],
  "experience_required": "string",
  "keywords": ["keyword1", "keyword2"]
}

Rules:
- If any field cannot be determined, return empty string "" for text fields or empty list [] for list fields.
- Return only raw JSON
- No markdown code blocks, no ```json wrapper
- No explanation before or after
- Start response with { and end with }
""",
)
