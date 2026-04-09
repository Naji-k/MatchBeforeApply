import os
from google.adk.agents import LlmAgent
from tools.web_scraper import scrape_url
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
    tools=[scrape_url],
    instruction="""You are a Job Description parser.

The user message contains the job description to parse. It starts with "jd_type: url" or "jd_type: text" followed by the content.

- If jd_type is "url": call the scrape_url tool with the URL, then parse the fetched content.
- If jd_type is "text": parse the content directly.

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

Return only the JSON. No markdown, no explanation.""",
)
