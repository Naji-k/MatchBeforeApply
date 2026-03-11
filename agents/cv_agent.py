from google.adk.agents import LlmAgent

cv_agent = LlmAgent(
    name="cv_agent",
    model="gemini-2.5-flash",
    output_key="cv_data",
    instruction="""You are a CV/Resume parser.

You will receive the raw text of a CV:
{cv_text}

Extract the following information and return ONLY a valid JSON object with no extra text:

{{
  "name": "string",
  "contact": {{
    "email": "string",
    "phone": "string",
    "linkedin": "string",
    "location": "string"
  }},
  "skills": ["skill1", "skill2"],
  "experience": [
    {{
      "title": "string",
      "company": "string",
      "duration": "string",
      "description": "string"
    }}
  ],
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
