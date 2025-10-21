from typing import List, Dict, Any, Optional


def calculate_average_word_count(competitor_analysis: List[Dict[str, Any]]) -> int:
    """Calculates the average word count from a list of competitor data."""
    word_counts = [
        c.get("word_count") for c in competitor_analysis if c and c.get("word_count")
    ]
    return int(sum(word_counts) / len(word_counts)) if word_counts else 1500


def calculate_average_readability(
    competitor_analysis: List[Dict[str, Any]],
) -> Optional[float]:
    """Calculates the average readability score from a list of competitor data."""
    readability_scores = [
        c.get("readability_score")
        for c in competitor_analysis
        if c.get("readability_score") is not None
    ]
    return (
        sum(readability_scores) / len(readability_scores)
        if readability_scores
        else None
    )
