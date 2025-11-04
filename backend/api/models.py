from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DiscoveryCostParams(BaseModel):
    seed_keywords: List[str]
    discovery_modes: Optional[List[str]] = ["ideas"]
    limit: Optional[int] = 1000
    include_clickstream_data: Optional[bool] = False
    people_also_ask_click_depth: Optional[int] = 0


# Define ContentUpdateRequest (W18 FIX)
class ContentUpdatePayload(BaseModel):
    article_body_html: str = Field(
        ..., description="The new HTML content for the article body."
    )


# Define ImageUpdatePayload (W18 FIX)
class ImageRegenRequest(BaseModel):
    original_prompt: str
    new_prompt: str


class DiscoveryRunRequest(BaseModel):
    seed_keywords: List[str]
    discovery_modes: Optional[List[str]] = Field(["keyword_ideas", "keyword_suggestions", "related_keywords"], description="List of DataForSEO Labs discovery modes to use.")
    filters: Optional[List[Any]] = Field(None, description="List of DataForSEO API filters to apply.")
    order_by: Optional[List[str]] = Field(None, description="List of DataForSEO API sorting rules.")
    filters_override: Optional[Dict[str, Any]] = Field({}, description="Key-value pairs to override specific client settings during discovery.")
    limit: Optional[int] = Field(100, ge=10, le=1000, description="Maximum number of keywords to return from each API source.")
    depth: Optional[int] = Field(1, ge=1, le=4, description="Discovery depth for 'Related Keywords' API (1-4).")
    exact_match: Optional[bool] = Field(False, description="If true, 'Keyword Suggestions' will only return exact phrase matches.")
    ignore_synonyms: Optional[bool] = Field(False, description="If true, exclude highly similar keywords from results.")
    include_clickstream_data: Optional[bool] = Field(False, description="If true, include clickstream-based metrics (doubles cost).")
    closely_variants: Optional[bool] = Field(False, description="If true, 'Keyword Ideas' uses phrase-match algorithm; otherwise, broad-match.")


class KeywordListRequest(BaseModel):
    seed_keywords: List[str]
    # NEW: Parameter for dynamic cost estimation
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


class GenerationOverrides(BaseModel):
    target_word_count: Optional[int] = None
    expert_persona: Optional[str] = None
    additional_instructions: Optional[str] = None


class ApproveAnalysisRequest(BaseModel):
    overrides: Optional[GenerationOverrides] = None
