"""
Ranking Service — ranks jobs by cosine similarity to user profile embedding.
"""
import json
from typing import List
import numpy as np

from app.services.embedding_service import embed_text
from app.utils.cosine import cosine_similarity
from app.utils.keyword_extractor import extract_keywords


async def rank_jobs_by_similarity(
    profile_embedding: List[float],
    jobs: List[dict],
    profile_skills: List[str],
    top_n: int = 25,
) -> List[dict]:
    """
    For each job, embed its description and compute cosine similarity
    against the user's profile embedding. Return top N ranked jobs.
    """
    profile_vec = np.array(profile_embedding)
    profile_skills_lower = {s.lower() for s in profile_skills}

    scored_jobs = []
    for job in jobs:
        description = job.get("description", "") or job.get("title", "")
        if not description:
            continue

        job_embedding = await embed_text(description[:2000])
        job_vec = np.array(job_embedding)
        similarity = cosine_similarity(profile_vec, job_vec)

        # Extract job keywords and compute skill overlap
        job_keywords = extract_keywords(description)
        matched_skills = [kw for kw in job_keywords if kw.lower() in profile_skills_lower]
        missing_skills = [kw for kw in job_keywords if kw.lower() not in profile_skills_lower]

        match_score = round(similarity * 100, 1)
        match_reasons = [f"Strong {s} overlap" for s in matched_skills[:3]]

        enriched = dict(job)
        enriched["match_score"] = match_score
        enriched["match_reasons"] = match_reasons
        enriched["missing_skills"] = missing_skills[:5]
        enriched["keywords"] = job_keywords

        scored_jobs.append(enriched)

    # Sort by match score descending
    scored_jobs.sort(key=lambda j: j["match_score"], reverse=True)
    return scored_jobs[:top_n]
