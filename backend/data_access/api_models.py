from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class KeywordInfoModel(BaseModel):
    """Strongly typed model for keyword_info from DataForSEO API."""
    se_type: str
    last_updated_time: str
    competition: float = Field(ge=0.0, le=1.0)
    competition_level: Optional[str] = Field(None, pattern="^(LOW|MEDIUM|HIGH)$")
    cpc: float = Field(ge=0.0)
    search_volume: int = Field(ge=0)
    low_top_of_page_bid: float = Field(ge=0.0)
    high_top_of_page_bid: float = Field(ge=0.0)
    categories: List[int] = []
    monthly_searches: List[Dict[str, int]] = []
    search_volume_trend: Dict[str, int] = {}
    
    @validator('competition', 'cpc', 'low_top_of_page_bid', 'high_top_of_page_bid', pre=True)
    def convert_to_float(cls, v):
        """Ensure numeric fields are floats."""
        if v is None:
            return 0.0
        return float(v)
    
    @validator('search_volume', pre=True)
    def convert_to_int(cls, v):
        """Ensure search volume is int."""
        if v is None:
            return 0
        return int(v)


class KeywordPropertiesModel(BaseModel):
    """Strongly typed model for keyword_properties from DataForSEO API."""
    se_type: str
    core_keyword: Optional[str] = None
    synonym_clustering_algorithm: Optional[str] = None
    keyword_difficulty: int = Field(ge=0, le=100)
    detected_language: str
    is_another_language: bool
    
    @validator('keyword_difficulty', pre=True)
    def convert_to_int(cls, v):
        if v is None:
            return 0
        return int(v)


class SerpInfoModel(BaseModel):
    """Strongly typed model for serp_info from DataForSEO API."""
    se_type: str
    check_url: Optional[str] = None
    serp_item_types: List[str] = []
    se_results_count: int = 0  # CRITICAL: Always int after sanitization
    last_updated_time: Optional[str] = None
    previous_updated_time: Optional[str] = None
    
    @validator('se_results_count', pre=True)
    def convert_se_results_count(cls, v):
        """
        CRITICAL FIX: se_results_count is STRING in Keyword Ideas/Suggestions API response.
        Per API docs, this field type varies by endpoint.
        """
        if v is None:
            return 0
        if isinstance(v, str):
            try:
                return int(v)
            except (ValueError, TypeError):
                return 0
        return int(v)


class SearchIntentInfoModel(BaseModel):
    """Strongly typed model for search_intent_info from DataForSEO API."""
    se_type: str
    main_intent: str = Field(pattern="^(informational|navigational|commercial|transactional)$")
    foreign_intent: Optional[List[str]] = None  # Can be null per API docs
    last_updated_time: Optional[str] = None
    
    @validator('foreign_intent', pre=True)
    def handle_null_foreign_intent(cls, v):
        """Per API docs: foreign_intent is null when there are no foreign intents."""
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return []


class AvgBacklinksInfoModel(BaseModel):
    """Strongly typed model for avg_backlinks_info from DataForSEO API."""
    se_type: str
    backlinks: float = 0.0
    dofollow: float = 0.0
    referring_pages: float = 0.0
    referring_domains: float = 0.0
    referring_main_domains: float = 0.0
    rank: float = 0.0
    main_domain_rank: float = 0.0
    last_updated_time: Optional[str] = None
    
    @validator('*', pre=True)
    def convert_to_float(cls, v):
        """Ensure all numeric fields are floats."""
        if v is None:
            return 0.0
        return float(v)
