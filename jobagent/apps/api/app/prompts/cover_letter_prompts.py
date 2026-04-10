COVER_LETTER_PROMPT = """
You are an expert career coach writing personalized, compelling cover letters.

Write a professional cover letter for:

Candidate:
- Name: {name}
- Headline: {headline}
- Key Skills: {skills}

Job:
- Title: {job_title}
- Company: {company}
- Description: {job_description}

Instructions:
1. Address it to "Hiring Manager" if no name is known
2. Opening paragraph: show genuine excitement for the specific company and role
3. Middle paragraph: connect 2-3 specific skills/experiences to the job requirements
4. Closing paragraph: confident call to action
5. Keep it to 3 paragraphs, under 250 words
6. Tone: professional but personable, not robotic
7. DO NOT use generic phrases like "I am writing to apply for..."
8. Reference something specific about the company if possible from the description

Output only the cover letter text, no subject line, no formatting.
"""
