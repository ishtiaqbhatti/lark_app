# data_mappers/serp_overview_mapper.py

from typing import Dict, Any
from data_access.models import SerpOverview


def map_serp_overview(raw_data: Dict[str, Any]) -> SerpOverview:
    """Maps raw SERP data from the DataForSEO API to the SerpOverview model."""
    serp_info = raw_data.get("serp_info", {})
    avg_backlinks_info = raw_data.get("avg_backlinks_info", {})

    return SerpOverview(
        serp_has_featured_snippet="featured_snippet"
        in serp_info.get("serp_item_types", []),
        serp_has_video_results="video" in serp_info.get("serp_item_types", []),
        serp_has_ai_overview="ai_overview" in serp_info.get("serp_item_types", []),
        people_also_ask=serp_info.get("people_also_ask", []),
        ai_overview_content=serp_info.get("ai_overview_content"),
        featured_snippet_content=serp_info.get("featured_snippet_content"),
        avg_referring_domains_top5_organic=avg_backlinks_info.get("referring_domains"),
        avg_main_domain_rank_top5_organic=avg_backlinks_info.get("main_domain_rank"),
        serp_last_updated_days_ago=serp_info.get("last_updated_time"),
        dominant_content_format=serp_info.get("dominant_content_format"),
    )
