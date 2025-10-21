from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class KeywordData:
    keyword: str
    search_volume: int
    keyword_difficulty: int
    main_intent: str
    cpc: float
    search_volume_trend: Optional[Dict[str, Any]] = None
    core_keyword: Optional[str] = None
    # Add other fields as they come from DataForSEO API


@dataclass
class CompetitorPage:
    url: str
    rank: int
    word_count: int
    readability_score: float
    technical_warnings: List[str] = field(default_factory=list)
    headings: Dict[str, List[str]] = field(default_factory=dict)
    full_content_plain_text: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SerpOverview:
    serp_has_featured_snippet: bool
    serp_has_video_results: bool
    serp_has_ai_overview: bool
    people_also_ask: List[str] = field(default_factory=list)
    ai_overview_content: Optional[str] = None
    featured_snippet_content: Optional[str] = None
    avg_referring_domains_top5_organic: Optional[float] = None
    avg_main_domain_rank_top5_organic: Optional[float] = None
    serp_last_updated_days_ago: Optional[int] = None
    dominant_content_format: Optional[str] = None


@dataclass
class ContentIntelligence:
    recommended_word_count: int
    average_readability_score: float
    common_headings_to_cover: List[str] = field(default_factory=list)
    unique_angles_to_include: List[str] = field(default_factory=list)
    ai_generated_outline_h2: List[str] = field(default_factory=list)
    ai_generated_outline_h3: List[str] = field(default_factory=list)


@dataclass
class AIBrief:
    target_keyword: str
    content_type: str
    target_audience_persona: str
    primary_goal: str
    target_word_count: int
    mandatory_sections: List[str] = field(default_factory=list)
    unique_angles_to_cover: List[str] = field(default_factory=list)
    questions_to_answer_directly: List[str] = field(default_factory=list)
    internal_linking_suggestions: List[Dict[str, str]] = field(default_factory=list)
    dynamic_serp_instructions: List[str] = field(default_factory=list)
    source_and_inspiration_content: Dict[str, Any] = field(default_factory=dict)
    client_id: str = "default"


@dataclass
class Blueprint:
    metadata: Dict[str, Any]
    winning_keyword: Dict[
        str, Any
    ]  # Full keyword data for the selected winning keyword
    serp_overview: SerpOverview
    content_intelligence: ContentIntelligence
    competitor_analysis: List[CompetitorPage]
    executive_summary: str
    ai_content_brief: AIBrief


@dataclass
class AIContentPackage:
    article_body_html: str
    meta_title: str
    meta_description: str
    social_blurbs: List[Dict[str, Any]]
    editor_notes: str
    ai_focus_keyword: str


@dataclass
class GeneratedImage:
    type: str  # 'featured' or 'in_article_N'
    original_prompt: str
    enhanced_prompt: str
    revised_prompt: str
    local_path: str
    model: str
    wordpress_id: Optional[int] = None
    remote_url: Optional[str] = None
    alt_text: Optional[str] = None
    insertion_marker: Optional[str] = None
    error: Optional[str] = None


@dataclass
class Opportunity:
    id: Optional[int]
    keyword: str  # This is the cluster_topic
    status: str
    client_id: str
    date_added: datetime
    date_processed: Optional[datetime]
    scheduled_for: Optional[datetime]
    full_data: Dict[str, Any]  # Original keyword data
    blueprint_data: Optional[Blueprint]
    ai_content_json: Optional[AIContentPackage]
    ai_content_model: Optional[str]
    featured_image_prompt: Optional[str]
    featured_image_model: Optional[str]
    featured_image_url: Optional[str]
    featured_image_local_path: Optional[str]
    in_article_images_data: List[GeneratedImage] = field(default_factory=list)
    wordpress_post_url: Optional[str]
    wordpress_post_id: Optional[int]
    social_media_posts_json: List[Dict[str, Any]] = field(default_factory=list)
    last_workflow_step: Optional[str]
    error_message: Optional[str]
    search_volume: Optional[int] = None
    keyword_difficulty: Optional[int] = None


@dataclass
class Client:
    client_id: str
    client_name: str
    date_created: datetime


@dataclass
class ClientSettings:
    client_id: str
    openai_api_key: Optional[str] = None
    pexels_api_key: Optional[str] = None  # NEW, was missing from dataclass
    wordpress_url: Optional[str] = None
    wordpress_user: Optional[str] = None
    wordpress_app_password: Optional[str] = None
    hootsuite_api_key: Optional[str] = None
    custom_ai_prompt_template: Optional[str] = None
    ai_image_style_formula: Optional[str] = None
    featured_image_base_prompt: Optional[str] = None
    wordpress_seo_plugin: Optional[str] = None
    ai_content_model: Optional[str] = None
    image_ai_model: Optional[str] = None
    num_in_article_images: Optional[int] = None
    image_quality: Optional[str] = None
    enable_automated_internal_linking: Optional[bool] = False
    default_wordpress_categories: List[str] = field(default_factory=list)
    default_wordpress_tags: List[str] = field(default_factory=list)
    negative_keywords: List[str] = field(default_factory=list)
    competitor_blacklist_domains: List[str] = field(default_factory=list)
    require_question_keywords: Optional[bool] = None
    enforce_intent_filter: Optional[bool] = None
    allowed_intents: List[str] = field(default_factory=list)
    max_competition_level: Optional[str] = None
    discovery_order_by: Optional[str] = None
    db_type: Optional[str] = "sqlite"  # NEW
    max_words_for_ai_analysis: Optional[int] = 1500  # NEW
    ai_generation_temperature: Optional[float] = 0.7  # NEW
    recommended_word_count_multiplier: Optional[float] = 1.2  # NEW
    max_avg_lcp_time: Optional[int] = 4000  # NEW
    prohibited_intents: List[str] = field(default_factory=list)  # NEW
    last_updated: datetime = field(default_factory=datetime.now)
