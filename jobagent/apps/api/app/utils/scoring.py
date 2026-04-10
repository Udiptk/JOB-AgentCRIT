def compute_coverage_score(matched: int, total: int) -> float:
    """Calculate the percentage score of matched keywords up to 100%."""
    if total <= 0:
        return 0.0
    return min((matched / total) * 100, 100.0)
