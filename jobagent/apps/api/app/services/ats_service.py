"""
ATS Service — computes ATS match score between resume and target job keywords.
"""
from typing import List, dict
from app.utils.keyword_extractor import extract_keywords, COMMON_JOB_KEYWORDS
from app.utils.scoring import compute_coverage_score


COMMON_ATS_SUGGESTIONS = [
    "Add measurable achievements with numbers and percentages.",
    "Include specific technologies and tools mentioned in the job description.",
    "Use action verbs at the start of bullet points.",
    "Add a dedicated Skills section with categorized skills.",
    "Ensure your contact information is at the top.",
]


async def compute_ats_score(
    resume_text: str,
    target_roles: List[str],
    resume_keywords: List[str],
) -> dict:
    """
    Compute an ATS score by comparing resume keywords
    to expected keywords for target roles.
    """
    # Get expected keywords for target roles
    target_text = " ".join(target_roles)
    expected_keywords = COMMON_JOB_KEYWORDS.get_for_roles(target_roles)

    resume_kw_lower = {kw.lower() for kw in resume_keywords}
    matched = [kw for kw in expected_keywords if kw.lower() in resume_kw_lower]
    missing = [kw for kw in expected_keywords if kw.lower() not in resume_kw_lower]

    score = compute_coverage_score(matched=len(matched), total=len(expected_keywords))
    coverage = round(len(matched) / max(len(expected_keywords), 1) * 100, 1)

    # Generate suggestions
    suggestions = []
    if missing:
        suggestions.append(f"Add these missing keywords: {', '.join(missing[:5])}")
    suggestions.extend(COMMON_ATS_SUGGESTIONS[:3])

    return {
        "score": score,
        "matched": matched[:20],
        "missing": missing[:20],
        "suggestions": suggestions,
        "coverage": coverage,
    }
