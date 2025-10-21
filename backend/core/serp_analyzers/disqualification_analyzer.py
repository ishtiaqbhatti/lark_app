# core/serp_analyzers/disqualification_analyzer.py
from typing import Dict, Any


class DisqualificationAnalyzer:
    def analyze(
        self, analysis: Dict[str, Any], config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Applies a set of granular rules to determine if a keyword should be disqualified.
        """
        disqualification_rules = config.get("disqualification_rules", {})

        # Rule: SERP is too crowded (pixel ranking)
        max_y_pixel = disqualification_rules.get("max_y_pixel_threshold")
        if max_y_pixel and analysis.get("first_organic_y_pixel") is not None:
            if analysis["first_organic_y_pixel"] > max_y_pixel:
                return {
                    "is_disqualified": True,
                    "disqualification_reason": f"First organic result is pushed down by {analysis['first_organic_y_pixel']} pixels, exceeding the {max_y_pixel}px threshold.",
                }

        # Rules based on page types in top 10
        top_10_results = analysis.get("top_organic_results", [])[:10]
        page_types = [result.get("page_type") for result in top_10_results]

        max_forum_results = disqualification_rules.get("max_forum_results_in_top_10")
        if (
            max_forum_results is not None
            and page_types.count("Forum") > max_forum_results
        ):
            return {
                "is_disqualified": True,
                "disqualification_reason": f"SERP contains {page_types.count('Forum')} forum results in the top 10, exceeding the threshold of {max_forum_results}.",
            }

        max_ecommerce_results = disqualification_rules.get(
            "max_ecommerce_results_in_top_10"
        )
        if (
            max_ecommerce_results is not None
            and page_types.count("E-commerce") > max_ecommerce_results
        ):
            return {
                "is_disqualified": True,
                "disqualification_reason": f"SERP contains {page_types.count('E-commerce')} e-commerce results in the top 10, exceeding the threshold of {max_ecommerce_results}.",
            }

        # Rule: Disallowed page types in top 3
        disallowed_in_top_3 = disqualification_rules.get(
            "disallowed_page_types_in_top_3", []
        )
        if disallowed_in_top_3:
            top_3_page_types = [
                result.get("page_type") for result in top_10_results[:3]
            ]
            for page_type in disallowed_in_top_3:
                if page_type in top_3_page_types:
                    return {
                        "is_disqualified": True,
                        "disqualification_reason": f"A '{page_type}' result was found in the top 3, which is a disallowed page type for high-ranking positions.",
                    }

        return {"is_disqualified": False, "disqualification_reason": None}
