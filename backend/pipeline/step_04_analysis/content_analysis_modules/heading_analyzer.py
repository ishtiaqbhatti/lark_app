from typing import List, Dict, Any
from collections import Counter


def extract_common_headings(
    competitor_analysis: List[Dict[str, Any]], num_headings: int
) -> List[str]:
    """Extracts the most common H2 and H3 headings from competitor data."""
    all_headings = Counter(
        h
        for c in competitor_analysis
        if c.get("headings")
        for h_type in ["h2", "h3"]
        for h in c["headings"].get(h_type, [])
    )
    return [h for h, count in all_headings.most_common(num_headings)]
