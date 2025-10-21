# core/serp_analyzers/video_analyzer.py

from typing import Dict, Any


class VideoAnalyzer:
    def analyze(self, serp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes the video results in the SERP."""
        analysis = {
            "serp_has_video_results": "video" in serp_data.get("item_types", [])
        }

        return analysis
