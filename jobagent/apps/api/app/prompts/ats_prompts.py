ATS_ANALYSIS_PROMPT = """
You are an ATS (Applicant Tracking System) expert. Analyze the following resume against the target role.

Resume:
{resume_text}

Target Role: {target_role}

Provide a JSON response with:
{{
  "score": <0-100>,
  "matched_keywords": ["keyword1", "keyword2", ...],
  "missing_keywords": ["keyword1", "keyword2", ...],
  "suggestions": [
    "Specific actionable suggestion 1",
    "Specific actionable suggestion 2",
    ...
  ],
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"]
}}

Be specific and practical. Focus on keywords that ATS systems commonly scan for in {target_role} roles.
"""

KEYWORD_EXTRACTION_PROMPT = """
Extract the top 20 technical and professional keywords from the following job description.
Focus on: technologies, tools, skills, methodologies, qualifications.

Job Description:
{job_description}

Return as a simple comma-separated list of keywords only, no explanation.
"""
