# data_mappers/keyword_data_mapper.py

from typing import Dict, Any
from data_access.models import KeywordData


def map_keyword_data(raw_data: Dict[str, Any]) -> KeywordData:
    """Maps raw keyword data from the DataForSEO API to the KeywordData model."""
    full_data = raw_data.get("full_data", {})
    keyword_info = full_data.get("keyword_info", {})
    keyword_properties = full_data.get("keyword_properties", {})
    search_intent_info = full_data.get("search_intent_info", {})

    return KeywordData(
        keyword=raw_data.get("keyword"),
        search_volume=keyword_info.get("search_volume"),
        keyword_difficulty=keyword_properties.get("keyword_difficulty"),
        cpc=keyword_info.get("cpc"),
        main_intent=search_intent_info.get("main_intent"),
        search_volume_trend=keyword_info.get("search_volume_trend"),
        core_keyword=keyword_properties.get("core_keyword"),
    )
