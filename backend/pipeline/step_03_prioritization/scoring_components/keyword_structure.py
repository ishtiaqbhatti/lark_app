# pipeline/step_03_prioritization/scoring_components/keyword_structure.py
from typing import Dict, Any, Tuple


def calculate_keyword_structure_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Scores the keyword based on its structure, rewarding the "long-tail sweet spot"
    and adding a bonus for search depth.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    keyword = data.get("keyword", "")
    word_count = len(keyword.split())
    depth = data.get("depth", 0)  # From related_keywords endpoint

    # Score is based on word count, with a peak at the 4-6 word sweet spot
    if word_count >= 4 and word_count <= 6:
        score = 100.0
    elif word_count == 3 or word_count == 7:
        score = 75.0
    elif word_count == 2 or word_count == 8:
        score = 50.0
    else:  # 1 word or 9+ words
        score = 25.0

    # Add a bonus for depth, rewarding more specific queries
    if depth > 0:
        score = min(100, score + (depth * 5))  # +5 points per depth level

    explanation = f"Keyword has {word_count} words and search depth of {depth}. The 4-6 word range is the sweet spot."
    breakdown = {
        "Keyword Structure": {
            "value": f"{word_count} words (Depth: {depth})",
            "score": score,
            "explanation": explanation,
        }
    }

    return score, breakdown
