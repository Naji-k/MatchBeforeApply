from google.adk.agents import LlmAgent


match_agent = LlmAgent(
    name="match_agent",
    model="gemini-2.5-flash",
    output_key="match_result",
    instruction="""You are a CV-to-Job match scorer.

You have the following data:

CV Data:
{cv_data}

Job Description Data:
{jd_data}

Compare the CV against the job description and return ONLY a valid JSON object with no extra text:

{{
  "overall_score": 0,
  "skills_score": 0,
  "experience_score": 0,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "summary": "2-3 sentence summary of how well the candidate fits the role"
}}

All scores are integers from 0 to 10 (10 being a perfect match). The overall_score should be an average of the skills_score and experience_score. The summary should be concise and informative.
Return only the JSON. No markdown, no explanation.""",
)
