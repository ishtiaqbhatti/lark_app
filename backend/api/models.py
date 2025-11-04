from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DiscoveryCostParams(BaseModel):
    seed_keywords: List[str]
    discovery_modes: Optional[List[str]] = ["ideas"]
    # NEW: Remove filters, order_by, filters_override from DiscoveryCostParams if they are not directly used here for cost calculation anymore
    # filters: Optional[List[Any]] = None
    # order_by: Optional[List[str]] = None
    # filters_override: Optional[Dict[str, Any]] = {}
    limit: Optional[int] = 1000
    include_clickstream_data: Optional[bool] = False
    people_also_ask_click_depth: Optional[int] = 0
    # NEW: Add discovery_goal for cost estimation if needed to fetch presets.
    discovery_goal: Optional[str] = None
    min_search_volume: Optional[int] = None
    max_keyword_difficulty: Optional[int] = None


class DiscoveryRunRequest(BaseModel):
    seed_keywords: List[str]
    discovery_modes: Optional[List[str]] = ["ideas"] # This will be overridden by client_cfg
    # REMOVED: `filters` as a direct input field. It's now generated from `discovery_goal`.
    # filters: Optional[List[Any]] = None
    order_by: Optional[List[str]] = None # This will be overridden by goal preset
    filters_override: Optional[Dict[str, Any]] = {} # Keep for advanced scenarios
    limit: Optional[int] = None
    depth: Optional[int] = None
    ignore_synonyms: Optional[bool] = False
    include_clickstream_data: Optional[bool] = None # NEW: Expose for user control
    closely_variants: Optional[bool] = None
    exact_match: Optional[bool] = None
    # NEW: Goal-based discovery fields
    discovery_goal: str = Field(..., description="The strategic goal for the discovery run.")
    min_search_volume: Optional[int] = None # User's custom SV or goal default
    max_keyword_difficulty: Optional[int] = None # User's custom KD or goal default


class KeywordListRequest(BaseModel):
    seed_keywords: List[str]
    include_clickstream_data: Optional[bool] = False


class JobResponse(BaseModel):
    job_id: str
    message: str
    status: Optional[str] = None
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress_log: Optional[List[Dict[str, Any]]] = None


class LoginRequest(BaseModel):
    password: str


class TemplateContent(BaseModel):
    name: str
    content: str
    description: Optional[str] = None


class TemplateResponse(BaseModel):
    name: str
    content: str
    description: Optional[str] = None
    last_updated: str


class PromptPreviewRequest(BaseModel):
    custom_template_content: Optional[str] = None


class PromptPreviewResponse(BaseModel):
    prompt: str


class ContentHistoryItem(BaseModel):
    id: int
    opportunity_id: int
    timestamp: str
    ai_content_json: Dict[str, Any]


class RestoreRequest(BaseModel):
    version_timestamp: str


class SingleImageRegenRequest(BaseModel):
    opportunity_id: int
    original_prompt: str
    new_prompt: str


class AutoWorkflowRequest(BaseModel):
    override_validation: bool = False


class SocialMediaPostsUpdate(BaseModel):
    social_media_posts: List[Dict[str, Any]]


class GlobalSettingsUpdate(BaseModel):
    settings: Dict[str, Any]


class OpportunityListResponse(BaseModel):
    items: List[Dict[str, Any]]
    total_items: int
    page: int
    limit: int


class AnalysisRequest(BaseModel):
    selected_competitor_urls: Optional[List[str]] = None


class RefineContentRequest(BaseModel):
    html_content: str
    command: str


class ClientSettings(BaseModel):
    brand_tone: Optional[str] = None
    target_audience: Optional[str] = None
    terms_to_avoid: Optional[str] = None
    # NEW: Add specific discovery settings fields from settings.ini
    # These map directly to fields in settings.ini [DISCOVERY_SETTINGS] and [DEFAULT]
    # The ConfigManager will handle loading them.
    discovery_strategies: Optional[List[str]] = Field(default_factory=list)
    deep_dive_discovery: Optional[bool] = None
    deep_dive_top_n_keywords: Optional[int] = None
    serp_feature_filters: Optional[List[str]] = Field(default_factory=list)
    load_async_ai_overview: Optional[bool] = None
    discovery_max_pages: Optional[int] = None
    people_also_ask_click_depth: Optional[int] = None
    serp_features_exclude_filter: Optional[List[str]] = Field(default_factory=list)
    closely_variants: Optional[bool] = None
    discovery_exact_match: Optional[bool] = None
    min_cpc_filter: Optional[float] = None
    max_cpc_filter: Optional[float] = None
    min_competition: Optional[float] = None
    max_competition: Optional[float] = None
    max_competition_level: Optional[str] = None
    discovery_ignore_synonyms: Optional[bool] = None
    search_phrase_regex: Optional[str] = None
    # From [DEFAULT] section
    include_clickstream_data: Optional[bool] = None
    # NEW: Add discovery_goals list
    discovery_goals: Optional[List[str]] = Field(default_factory=list)

    # From [SEO_CRITERIA] for global defaults
    location_code: Optional[int] = None
    language_code: Optional[str] = None
    target_domain: Optional[str] = None
    device: Optional[str] = None
    os: Optional[str] = None

    # From [AI_MODEL_SETTINGS] or similar
    ai_content_model: Optional[str] = None
    ai_generation_temperature: Optional[float] = None
    expert_persona: Optional[str] = None
    recommended_word_count_multiplier: Optional[float] = None
    max_completion_tokens_for_generation: Optional[int] = None
    max_words_for_ai_analysis: Optional[int] = None
    custom_prompt_template: Optional[str] = None
    client_knowledge_base: Optional[str] = None # Assuming this will be managed via client settings

    # Image generation settings
    use_pexels_first: Optional[bool] = None
    num_in_article_images: Optional[int] = None
    overlay_text_enabled: Optional[bool] = None
    overlay_text_color: Optional[str] = None
    overlay_background_color: Optional[str] = None
    overlay_font_size: Optional[int] = None
    overlay_position: Optional[str] = None

    # OnPage API client config settings
    onpage_enable_javascript: Optional[bool] = None
    onpage_load_resources: Optional[bool] = None
    onpage_disable_cookie_popup: Optional[bool] = None
    onpage_return_despite_timeout: Optional[bool] = None
    onpage_enable_browser_rendering: Optional[bool] = None
    onpage_store_raw_html: Optional[bool] = None
    onpage_validate_micromarkup: Optional[bool] = None
    onpage_check_spell: Optional[bool] = None
    onpage_accept_language: Optional[str] = None
    onpage_custom_user_agent: Optional[str] = None
    onpage_max_domains_per_request: Optional[int] = None
    onpage_max_tasks_per_request: Optional[int] = None
    onpage_enable_switch_pool: Optional[bool] = None
    ip_pool_for_scan: Optional[str] = None # assuming str type
    onpage_enable_custom_js: Optional[bool] = None
    onpage_custom_js: Optional[str] = None
    onpage_browser_screen_resolution_ratio: Optional[float] = None
    onpage_custom_checks_thresholds: Optional[str] = None # assuming str type for JSON

    # Scoring Weights
    ease_of_ranking_weight: Optional[float] = None
    traffic_potential_weight: Optional[float] = None
    commercial_intent_weight: Optional[float] = None
    serp_features_weight: Optional[float] = None
    growth_trend_weight: Optional[float] = None
    serp_freshness_weight: Optional[float] = None
    serp_volatility_weight: Optional[float] = None
    competitor_weakness_weight: Optional[float] = None
    competitor_performance_weight: Optional[float] = None

    # Scoring Normalization
    max_cpc_for_scoring: Optional[float] = None
    max_sv_for_scoring: Optional[int] = None
    max_domain_rank_for_scoring: Optional[int] = None
    max_referring_domains_for_scoring: Optional[int] = None

    # Disqualification Rules
    min_search_volume: Optional[int] = None
    max_keyword_difficulty: Optional[int] = None
    prohibited_intents: Optional[List[str]] = Field(default_factory=list)
    negative_keywords: Optional[List[str]] = Field(default_factory=list)
    yearly_trend_decline_threshold: Optional[int] = None
    quarterly_trend_decline_threshold: Optional[int] = None
    search_volume_volatility_threshold: Optional[float] = None
    max_paid_competition_score: Optional[float] = None
    max_high_top_of_page_bid: Optional[float] = None
    max_kd_hard_limit: Optional[int] = None
    max_referring_main_domains_limit: Optional[int] = None
    max_avg_domain_rank_threshold: Optional[int] = None
    max_pages_to_domain_ratio: Optional[float] = None
    hostile_serp_features: Optional[List[str]] = Field(default_factory=list)
    crowded_serp_features_threshold: Optional[int] = None
    min_serp_stability_days: Optional[int] = None
    max_y_pixel_threshold: Optional[int] = None
    max_forum_results_in_top_10: Optional[int] = None
    max_ecommerce_results_in_top_10: Optional[int] = None
    disallowed_page_types_in_top_3: Optional[List[str]] = Field(default_factory=list)
    min_keyword_word_count: Optional[int] = None
    max_keyword_word_count: Optional[int] = None
    high_value_sv_override_threshold: Optional[int] = None
    high_value_cpc_override_threshold: Optional[float] = None
    non_evergreen_year_pattern: Optional[str] = None
    
    # Validation
    disable_ai_overview_check: Optional[bool] = None
    max_non_blog_results: Optional[int] = None
    max_ai_overview_words: Optional[int] = None
    max_first_organic_y_pixel: Optional[int] = None
    final_validation_non_blog_domains: Optional[List[str]] = Field(default_factory=list)
    max_avg_lcp_time: Optional[int] = None

    last_updated: Optional[str] = None


class GenerationOverrides(BaseModel):
    target_word_count: Optional[int] = None
    expert_persona: Optional[str] = None
    additional_instructions: Optional[str] = None


class ApproveAnalysisRequest(BaseModel):
    overrides: Optional[GenerationOverrides] = None


class ContentUpdatePayload(BaseModel):
    article_body_html: str


class DiscoveryRunResponse(BaseModel):
    items: List[Dict[str, Any]]
    total_items: int
    page: int
    limit: int
