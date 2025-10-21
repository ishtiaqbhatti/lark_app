# pipeline/step_03_prioritization/scoring_components/volume_volatility.py
import numpy as np
from typing import Dict, Any, Tuple


def calculate_volume_volatility_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on the stability of monthly search volume.
    Lower volatility is generally better for long-term planning.
    """
    if not isinstance(data, dict):
        return 50.0, {
            "Volatility": {
                "value": "N/A",
                "score": 50,
                "explanation": "Invalid data format.",
            }
        }

    keyword_info = (
        data.get("keyword_info") if isinstance(data.get("keyword_info"), dict) else {}
    )
    monthly_searches = keyword_info.get("monthly_searches", [])

    if not monthly_searches or len(monthly_searches) < 3:
        return 50.0, {
            "Volatility": {
                "value": "N/A",
                "score": 50,
                "explanation": "Insufficient data.",
            }
        }

    volumes = [
        ms["search_volume"]
        for ms in monthly_searches
        if isinstance(ms, dict)
        and ms.get("search_volume") is not None
        and ms["search_volume"] > 0
    ]
    if len(volumes) < 3:
        return 50.0, {
            "Volatility": {
                "value": "N/A",
                "score": 50,
                "explanation": "Insufficient data.",
            }
        }

    mean_volume = np.mean(volumes)
    std_dev = np.std(volumes)

    if mean_volume == 0:
        return 0.0, {
            "Volatility": {"value": "0", "score": 0, "explanation": "No search volume."}
        }

    coeff_of_variation = std_dev / mean_volume

    # Score is inverted: higher volatility = lower score
    # A CoV of 0.5 (50%) is considered moderately high.
    score = max(0, 100 - (coeff_of_variation * 150))  # Scale the penalty

    explanation = (
        f"Coefficient of Variation: {coeff_of_variation:.2%}. Lower is more stable."
    )
    breakdown = {
        "Volatility": {
            "value": f"{coeff_of_variation:.2%}",
            "score": round(score),
            "explanation": explanation,
        }
    }

    return round(score), breakdown
