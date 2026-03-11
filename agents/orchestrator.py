from google.adk.agents import SequentialAgent

from agents.jd_agent import jd_agent
from agents.cv_agent import cv_agent
from agents.match_agent import match_agent
from agents.ats_agent import ats_agent

root_agent = SequentialAgent(
    name="cv_job_matcher",
    sub_agents=[
        jd_agent,
        cv_agent,
        match_agent,
        ats_agent,
    ],
)
