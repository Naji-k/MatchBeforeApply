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

You will receive:
- jd_type: "{jd_type}" — either "url" or "text"
- jd_input: "{jd_input}" — a URL or plain text job description

If jd_type is "url", call the scrape_url tool with jd_input to fetch the page content first.
If jd_type is "text", use jd_input directly as the job description.

Extract the following information and return ONLY a valid JSON object with no extra text:

{{
  "job_title": "string",
  "company": "string",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill1", "skill2"],
  "nice_to_have": ["skill1", "skill2"],
  "experience_required": "string",
  "keywords": ["keyword1", "keyword2"]
}}

Return only the JSON. No markdown, no explanation, """,
)
