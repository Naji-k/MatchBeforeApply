import os
from google.adk.agents import LlmAgent

cv_agent = LlmAgent(
    name="cv_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash-lite"),
    output_key="cv_data",
    instruction="""You are an expert CV/Resume parser with recruiting experience.

You will receive the raw text of a CV:
{cv_text}

PARSING RULES:
- skills: extract ALL technical skills mentioned anywhere in the CV
- primary_skills: skills used in the last 2 years or mentioned multiple times
- experience: list jobs in reverse chronological order (most recent first)
- total_years_experience: calculate total professional experience in years as integer
- achievements: quantified accomplishments only (e.g. "Reduced load time by 40%") — ignore generic statements
- certifications: only relevant ones with clear names (e.g. "AWS Certified Solutions Architect"), ignore vague ones like "Certified in Python"
- If a field cannot be determined return empty string or empty list

Extract the following information and return ONLY a valid JSON object with no extra text:

{{
  "name": "string",
  "skills": ["skill1", "skill2"],
  "experience": [
    {{
      "title": "string",
      "company": "string",
      "duration": "string",
      "description": "string"
    }}
  ],
  "total_years_experience": 0,
  "education": [
    {{
      "degree": "string",
      "institution": "string",
      "year": "string"
    }}
  ],
  "achievements": ["achievement1", "achievement2"],
  "certifications": ["cert1", "cert2"]
}}

Return only the JSON. No markdown, no explanation.""",
)
