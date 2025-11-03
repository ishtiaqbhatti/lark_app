You are absolutely right. My apologies for the previous fragmented responses. You need a **single, comprehensive, standalone output** with every granular step and every single line of code explicitly provided. There will be **no placeholders** and **no references to previous outputs**.

This plan integrates all previous feedback and corrections, including:
1.  **Efficient AI Interaction:** The clustering AI call is optimized to handle reconciliation in one go.
2.  **Clear Status Feedback:** Keywords will show an "clustering" status during processing.
3.  **Professional Notifications:** `react-hot-toast` is integrated for non-blocking user feedback.
4.  **Robust Database Sessions:** Correct SQLAlchemy session management for background tasks.
5.  **Optimized Frontend Data Fetching:** Dedicated API endpoints for clustered and unclustered keywords.

---

## **Final Implementation Plan: Automated Keyword Clustering & Batch Content Generation**

This document provides a complete, step-by-step implementation plan with all necessary code changes. Execute the terminal commands and update the specified files exactly as shown.

---

### **I. Prerequisites & Initial Setup (Terminal Commands)**

**Action:** Execute these commands in your terminal *before* modifying any code files.

1.  **Navigate to the `frontend` directory and install `react-hot-toast`:**
    ```bash
    cd frontend
    npm install react-hot-toast
    ```
2.  **Navigate back to the `backend` directory:**
    ```bash
    cd ../backend
    ```
3.  **After all `backend/app/models.py` changes (Step II.A.1) are applied, generate and apply the database migration:**
    *(You may need to inspect the generated migration file for correctness before applying it in a production environment.)*
    ```bash
    alembic revision --autogenerate -m "Add keyword cluster tables and clustering status"
    alembic upgrade head
    ```

---

### **II. Backend Implementation (Database, Schemas, AI Service, Workflows, APIs)**

#### **A. Database & Schemas**

#### **Granular Step II.A.1: Update Database Models (`backend/app/models.py`)**

**Action:** Add the `keyword_cluster_association` table, the `KeywordCluster` model, and modify `Site` and `Keyword` relationships/status.

**File:** `backend/app/models.py`

```python
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# ADDED: New association table for many-to-many relationship between keywords and clusters
keyword_cluster_association = Table(
    'keyword_cluster_association',
    Base.metadata,
    Column('keyword_id', String, ForeignKey('keywords.id'), primary_key=True),
    Column('cluster_id', String, ForeignKey('keyword_clusters.id'), primary_key=True)
)

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False)
    wordpress_url = Column(String(500), nullable=False)
    wordpress_username = Column(String(255))
    wordpress_app_password = Column(Text)
    hootsuite_access_token = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    keywords = relationship("Keyword", back_populates="site")
    content = relationship("Content", back_populates="site")
    clusters = relationship("KeywordCluster", back_populates="site") # MODIFIED: Add relationship to KeywordCluster

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    keyword = Column(Text, nullable=False)
    search_volume = Column(Integer)
    keyword_difficulty = Column(Integer)
    cpc = Column(Float)
    competition_level = Column(String(20))
    main_intent = Column(String(50))
    serp_features = Column(JSON)
    strategic_score = Column(Float)
    
    # MODIFIED: Added 'clustering' status for UI feedback during the clustering process
    status = Column(String(50), default='discovered')  # discovered, qualified, clustering, analyzing, generating, completed, failed
    progress = Column(Integer, default=0)
    error_message = Column(Text)
    
    # Cost tracking
    discovery_cost = Column(Float, default=0.0)
    analysis_cost = Column(Float, default=0.0)
    generation_cost = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site", back_populates="keywords")
    content = relationship("Content", back_populates="keyword", uselist=False)
    competitor_analysis = relationship("CompetitorAnalysis", back_populates="keyword", uselist=False)
    clusters = relationship( # MODIFIED: Add relationship to KeywordCluster
        "KeywordCluster",
        secondary=keyword_cluster_association,
        back_populates="keywords"
    )

# ADDED: New KeywordCluster Model
class KeywordCluster(Base):
    __tablename__ = "keyword_clusters"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    site = relationship("Site", back_populates="clusters")
    keywords = relationship(
        "Keyword",
        secondary=keyword_cluster_association,
        back_populates="keywords"
    )

class CompetitorAnalysis(Base):
    __tablename__ = "competitor_analysis"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    keyword_id = Column(String, ForeignKey("keywords.id"), nullable=False)
    top_urls = Column(JSON)
    analysis_data = Column(JSON)
    content_blueprint = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    keyword = relationship("Keyword", back_populates="competitor_analysis")

class Content(Base):
    __tablename__ = "content"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    keyword_id = Column(String, ForeignKey("keywords.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    
    title = Column(Text)
    meta_description = Column(Text)
    body = Column(Text)
    images = Column(JSON)
    social_posts = Column(JSON)
    
    wordpress_post_id = Column(Integer)
    wordpress_url = Column(String(500))
    
    status = Column(String(50), default='draft')  # draft, published, failed
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    site = relationship("Site", back_populates="content")
    keyword = relationship("Keyword", back_populates="content")

class APIUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    provider = Column(String(50), nullable=False)
    endpoint = Column(String(255), nullable=False)
    cost = Column(Float, nullable=False)
    tokens_used = Column(Integer)
    usage_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### **Granular Step II.A.2: Update Pydantic Schemas (`backend/app/schemas.py`)**

**Action:** Add the `KeywordClusterResponse` schema.

**File:** `backend/app/schemas.py`

```python
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime

# Site Schemas
class SiteCreate(BaseModel):
    name: str
    domain: str
    wordpress_url: str
    wordpress_username: str
    wordpress_app_password: str
    hootsuite_access_token: Optional[str] = None

class SiteResponse(BaseModel):
    id: str
    name: str
    domain: str
    wordpress_url: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Keyword Schemas
class KeywordDiscoveryRequest(BaseModel):
    site_id: str
    seed_keywords: List[str]
    min_search_volume: Optional[int] = 500
    max_keyword_difficulty: Optional[int] = 20
    intent: Optional[str] = "informational"
    limit: Optional[int] = 50

class KeywordResponse(BaseModel):
    id: str
    keyword: str
    search_volume: Optional[int]
    keyword_difficulty: Optional[int]
    cpc: Optional[float]
    strategic_score: Optional[float]
    status: str
    progress: int
    error_message: Optional[str] # ADDED: Ensure error_message is included
    
    class Config:
        from_attributes = True

# Content Schemas
class ContentGenerationRequest(BaseModel):
    keyword_id: str
    custom_prompt: Optional[str] = None

class ContentListResponse(BaseModel):
    id: str
    keyword_id: str
    title: Optional[str]
    meta_description: Optional[str]
    status: str
    wordpress_url: Optional[str]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class FullContent(BaseModel):
    id: str
    keyword_id: str
    title: Optional[str]
    body: Optional[str]
    meta_description: Optional[str]
    status: str
    wordpress_url: Optional[str]
    published_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# ADDED: Keyword Cluster Schema
class KeywordClusterResponse(BaseModel):
    id: str
    name: str
    keywords: List[KeywordResponse]

    class Config:
        from_attributes = True

# Analytics Schema
class CostAnalytics(BaseModel):
    total_spent: float
    remaining_budget: float
    avg_cost_per_article: float
    articles_generated: int
```

#### **Granular Step II.A.3: Enhance AI Service with Batch Reconciliation (`backend/app/services/openai_service.py`)**

**Action:** Replace `cluster_keywords` and `reconcile_cluster_name` with a single, optimized `cluster_keywords_with_reconciliation` method.

**File:** `backend/app/services/openai_service.py`

```python
from openai import OpenAI
from typing import Dict, List
import json
from app.config import settings
from app.services.cost_tracker import CostTracker
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """OpenAI service with cost tracking"""
    
    INPUT_COST_PER_1M = 5.00
    OUTPUT_COST_PER_1M = 15.00
    
    def __init__(self, cost_tracker: CostTracker):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.cost_tracker = cost_tracker
    
    async def analyze_competitors(
        self,
        keyword: str,
        competitor_data: List[Dict]
    ) -> Dict:
        """Analyze competitor content and create strategy"""
        
        competitor_summary = "\n".join([
            f"- {c.get('title', 'N/A')} ({c.get('word_count', 0)} words)"
            for c in competitor_data
        ])
        
        prompt = f"""Analyze these top-ranking articles for the keyword "{keyword}":

{competitor_summary}

Provide a strategic analysis in JSON format:
1. Common themes across all articles
2. Content gaps (topics they miss)
3. Optimal word count recommendation
4. Key headings to include
5. Unique angles to take
"""
        
        model = "gpt-4o-2024-08-06"
        logger.info(f"Analyzing competitors for '{keyword}' using model {model}")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert SEO strategist."}, 
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "competitor_analysis",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "common_themes": {"type": "array", "items": {"type": "string"}},
                            "content_gaps": {"type": "array", "items": {"type": "string"}},
                            "recommended_word_count": {"type": "integer"},
                            "key_headings": {"type": "array", "items": {"type": "string"}},
                            "unique_angles": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["common_themes", "content_gaps", "recommended_word_count", "key_headings", "unique_angles"],
                        "additionalProperties": False
                    }
                }
            }
        )
        
        usage = response.usage
        cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)
        logger.info(
            f"Competitor analysis complete. Tokens used: {usage.total_tokens}, Cost: ${cost:.6f}"
        )
        
        await self.cost_tracker.log_usage(
            provider="openai",
            endpoint="competitor_analysis",
            cost=cost,
            tokens_used=usage.total_tokens
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def generate_article(
        self,
        keyword: str,
        analysis: Dict,
        custom_prompt: str = None
    ) -> Dict:
        """Generate blog post content"""
        
        system_prompt = custom_prompt or f"""You are an expert SEO content writer. Write a comprehensive blog post on "{keyword}".

Requirements:
- Target keyword: {keyword}
- Word count: {analysis.get('recommended_word_count', 1200)} words
- Include these headings: {', '.join(analysis.get('key_headings', [])[:5])}
- Cover these content gaps: {', '.join(analysis.get('content_gaps', [])[:3])}
- Unique angles: {', '.join(analysis.get('unique_angles', [])[:2])}
- Include FAQ section at the end
- Natural CTA to https://profitparrot.com/contact/
- Keyword density: 1.2%
- Human-sounding, helpful tone
"""
        
        model = "gpt-4o-2024-08-06"
        logger.info(f"Generating article for '{keyword}' using model {model}")

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write the blog post for: {keyword}"}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "blog_post",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "meta_description": {"type": "string"},
                            "body": {"type": "string"}
                        },
                        "required": ["title", "meta_description", "body"],
                        "additionalProperties": False
                    }
                }
            }
        )
        
        usage = response.usage
        cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)
        logger.info(
            f"Article generation complete. Tokens used: {usage.total_tokens}, Cost: ${cost:.6f}"
        )
        
        await self.cost_tracker.log_usage(
            provider="openai",
            endpoint="article_generation",
            cost=cost,
            tokens_used=usage.total_tokens
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def generate_social_posts(
        self,
        title: str,
        article_url: str
    ) -> Dict:
        """Generate platform-specific social media posts"""
        
        prompt = f"""Create social media posts for this article:
Title: {title}
URL: {article_url}

Generate posts for: Facebook, LinkedIn, Twitter, Google Business Profile
Each should be optimized for that platform's best practices.
"""
        
        model = "gpt-4o-2024-08-06"
        logger.info(f"Generating social posts for article: '{title}' using model {model}")

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a social media expert."}, 
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "social_posts",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "facebook": {"type": "string"},
                            "linkedin": {"type": "string"},
                            "twitter": {"type": "string"},
                            "google_business": {"type": "string"}
                        },
                        "required": ["facebook", "linkedin", "twitter", "google_business"],
                        "additionalProperties": False
                    }
                }
            }
        )
        
        usage = response.usage
        cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)
        logger.info(
            f"Social post generation complete. Tokens used: {usage.total_tokens}, Cost: ${cost:.6f}"
        )
        
        await self.cost_tracker.log_usage(
            provider="openai",
            endpoint="social_posts",
            cost=cost,
            tokens_used=usage.total_tokens
        )
        
        return json.loads(response.choices[0].message.content)

    # ADDED: Combined clustering and reconciliation method (efficient AI call)
    async def cluster_keywords_with_reconciliation(
        self, keywords_to_cluster: List[str], existing_cluster_names: List[str]
    ) -> Dict[str, List[str]]:
        """
        Clusters new keywords and reconciles them against existing cluster names in a single AI call.
        """
        keyword_list_str = "\n".join([f"- {kw}" for kw in keywords_to_cluster])
        existing_names_str = ", ".join(existing_cluster_names) if existing_cluster_names else "None"

        prompt = f"""You are an expert SEO strategist. Here is a list of new keywords to cluster:
{keyword_list_str}

Here is a list of existing cluster names on the site:
{existing_names_str}

Your task is to group the new keywords into semantic clusters. For each group of new keywords, decide if it belongs to one of the existing clusters.
- If a new group's topic matches an existing cluster, use the EXISTING cluster name as the key.
- If a new group's topic is genuinely new, create a new, concise cluster name (2-4 words) for it.
- Group any single, unrelated keywords into a 'Miscellaneous' cluster.

Return a single JSON object where keys are the final cluster names (either existing or new) and values are the keywords belonging to that cluster.
"""
        
        model = "gpt-4o-2024-08-06"
        logger.info(f"Clustering {len(keywords_to_cluster)} keywords against {len(existing_cluster_names)} existing clusters.")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert SEO strategist specializing in topic clustering and reconciliation. Your output must strictly adhere to the JSON schema."},
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "keyword_clusters",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "description": "A dictionary where keys are cluster names and values are lists of keywords.",
                        "patternProperties": {
                            "^[a-zA-Z0-9 ]+$": { # Allow alphanumeric and spaces for cluster names
                                "type": "array",
                                "items": { "type": "string" }
                            }
                        },
                        "additionalProperties": False
                    }
                }
            }
        )
        
        usage = response.usage
        cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)
        logger.info(
            f"Keyword clustering and reconciliation complete. Tokens used: {usage.total_tokens}, Cost: ${cost:.6f}"
        )
        
        await self.cost_tracker.log_usage(
            provider="openai",
            endpoint="keyword_clustering_reconciliation",
            cost=cost,
            tokens_used=usage.total_tokens
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD"""
        input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_1M
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_1M
        return round(input_cost + output_cost, 6)
```

#### **B. Workflows**

#### **Granular Step II.B.1: Create Clustering Workflow (`backend/app/workflows/keyword_clustering.py`)**

**Action:** Create the core logic to cluster keywords, handle reconciliation, and link them.

**File:** `backend/app/workflows/keyword_clustering.py`

```python
from sqlalchemy.orm import Session
from app.models import Keyword, KeywordCluster, keyword_cluster_association
from app.services.openai_service import OpenAIService
from app.services.cost_tracker import CostTracker
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class KeywordClusteringWorkflow:
    def __init__(self, db: Session):
        self.db = db
        self.cost_tracker = CostTracker(db)
        self.openai = OpenAIService(self.cost_tracker)

    async def cluster_and_save(self, site_id: str):
        """
        Retrieves all UNCLUSTERED, qualified/completed keywords for a site,
        clusters them using AI, and saves the associations.
        """
        unclustered_keywords = (
            self.db.query(Keyword)
            .filter(Keyword.site_id == site_id)
            .filter(Keyword.status.in_(['qualified', 'completed'])) # Only cluster qualified or completed keywords
            .outerjoin(keyword_cluster_association)
            .filter(keyword_cluster_association.c.cluster_id == None)
            .all()
        )
        
        if not unclustered_keywords:
            logger.info(f"No new qualified keywords to cluster for site {site_id}.")
            return

        # MODIFIED: Set status to 'clustering' for immediate UI feedback
        for kw in unclustered_keywords:
            kw.status = 'clustering'
        self.db.commit() # Commit the status change immediately

        try:
            keyword_map: Dict[str, Keyword] = {kw.keyword: kw for kw in unclustered_keywords}
            keyword_strings = [kw.keyword for kw in unclustered_keywords]
            
            existing_clusters = self.db.query(KeywordCluster).filter_by(site_id=site_id).all()
            existing_cluster_names = [c.name for c in existing_clusters] # Use a copy for AI prompt
            existing_cluster_map: Dict[str, KeywordCluster] = {c.name: c for c in existing_clusters}

            # MODIFIED: Single, efficient AI call for clustering and reconciliation
            ai_clusters = await self.openai.cluster_keywords_with_reconciliation(
                keyword_strings, existing_cluster_names
            )

            for final_cluster_name, keywords_in_cluster in ai_clusters.items():
                if not keywords_in_cluster:
                    continue

                cluster = existing_cluster_map.get(final_cluster_name)
                if not cluster:
                    cluster = KeywordCluster(name=final_cluster_name, site_id=site_id)
                    self.db.add(cluster)
                    self.db.flush() # Flush to get cluster.id for relationship association
                    existing_cluster_map[final_cluster_name] = cluster # Add to map for subsequent reconciliation hits
                
                for keyword_str in keywords_in_cluster:
                    if keyword_str in keyword_map:
                        keyword_obj = keyword_map[keyword_str]
                        # Only add if not already associated (prevents duplicates on re-run)
                        if keyword_obj not in cluster.keywords:
                            cluster.keywords.append(keyword_obj)
                        # Revert status to 'qualified' after successful clustering
                        keyword_obj.status = 'qualified'
            
            self.db.commit()
            logger.info(f"Successfully clustered and saved keywords for site {site_id}.")

        except Exception as e:
            logger.error(f"Clustering workflow failed for site {site_id}: {e}", exc_info=True)
            self.db.rollback() # Rollback any changes from this transaction on failure
            # Revert status of all keywords that were set to 'clustering' back to 'qualified' on failure
            for kw in unclustered_keywords:
                kw.status = 'qualified'
            self.db.commit()
            raise
```

#### **Granular Step II.B.2: Create Batch Generator Workflow (`backend/app/workflows/cluster_generator.py`)**

**Action:** Create the workflow to queue `ContentGeneratorWorkflow` tasks for all qualified keywords in a cluster.

**File:** `backend/app/workflows/cluster_generator.py`

```python
from sqlalchemy.orm import Session, sessionmaker
from app.models import Keyword, KeywordCluster
from app.workflows.content_generator import ContentGeneratorWorkflow
from app.services.cost_tracker import CostTracker
import logging
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)

class ClusterGeneratorWorkflow:
    def __init__(self, db_engine: object, background_tasks: BackgroundTasks):
        """
        Initializes the workflow. db_engine is expected to be a SQLAlchemy engine 
        (e.g., from app.database.engine) to allow creating new sessions for
        each background task.
        """
        self.db_engine = db_engine
        self.background_tasks = background_tasks
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.db_engine)

    async def generate_for_cluster(self, cluster_id: str):
        """
        Iterates through a cluster and triggers content generation for all 
        qualified keywords.
        """
        # Fetch cluster data within a dedicated session for this initial function scope
        db_for_fetch = self.SessionLocal()
        try:
            cluster = db_for_fetch.query(KeywordCluster).filter_by(id=cluster_id).first()
            if not cluster:
                logger.error(f"Cluster {cluster_id} not found.")
                raise Exception(f"Cluster {cluster_id} not found.")

            qualified_keywords = [
                kw for kw in cluster.keywords 
                if kw.status == 'qualified'
            ]
        finally:
            db_for_fetch.close()

        if not qualified_keywords:
            logger.info(f"No qualified keywords in cluster {cluster.name}. No content generation tasks to queue.")
            return
        
        # Check budget using a temporary session
        temp_session_for_cost = self.SessionLocal()
        try:
            cost_tracker = CostTracker(temp_session_for_cost)
            estimated_cost_per_article = 0.15 # Max estimated cost per article from ContentGeneratorWorkflow
            total_estimated_cost = len(qualified_keywords) * estimated_cost_per_article

            if not await cost_tracker.can_proceed(total_estimated_cost):
                raise Exception(f"Monthly budget exceeded (Est: ${total_estimated_cost:.2f}). Cannot proceed with batch content generation.")
        finally:
            temp_session_for_cost.close()

        logger.info(f"Queuing {len(qualified_keywords)} individual content generation tasks for cluster: {cluster.name}")
        
        # Sequentially add generation tasks to the background queue
        for keyword in qualified_keywords:
            
            # Define the async function for a single content generation
            async def run_single_generation_task(keyword_id: str, cluster_name_for_log: str):
                # IMPORTANT: Each background task MUST get its own SQLAlchemy session
                db_session_for_task = self.SessionLocal()
                try:
                    # The ContentGeneratorWorkflow encapsulates the full pipeline
                    workflow = ContentGeneratorWorkflow(db_session_for_task)
                    await workflow.generate_complete_article(
                        keyword_id=keyword_id,
                        custom_prompt=None # No custom prompt for batch generation
                    )
                except Exception as e:
                    logger.error(f"Single content generation failed for keyword '{keyword_id}' in cluster '{cluster_name_for_log}': {e}", exc_info=True)
                    # Update keyword status to failed if an error occurred during its individual generation
                    failed_keyword = db_session_for_task.query(Keyword).filter_by(id=keyword_id).first()
                    if failed_keyword:
                        failed_keyword.status = 'failed'
                        failed_keyword.error_message = f"Batch generation failed: {str(e)}"
                        db_session_for_task.commit()
                finally:
                    db_session_for_task.close()

            # Add each generation to FastAPI's BackgroundTasks
            self.background_tasks.add_task(run_single_generation_task, keyword.id, cluster.name)
```

#### **C. API Endpoints**

#### **Granular Step II.C.1: Add `list_unclustered_keywords` to `backend/app/api/keywords.py`**

**Action:** Add a new endpoint to efficiently retrieve keywords that are not yet assigned to any cluster.

**File:** `backend/app/api/keywords.py`

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Keyword, keyword_cluster_association # MODIFIED: Added keyword_cluster_association for join
from app.schemas import KeywordDiscoveryRequest, KeywordResponse
from app.workflows.keyword_discovery import KeywordDiscoveryWorkflow
from typing import List

router = APIRouter(prefix="/api/keywords", tags=["Keywords"])

@router.post("/discover", response_model=dict)
async def discover_keywords(
    request: KeywordDiscoveryRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Discover and qualify keywords
    Returns immediately, runs in background
    """
    
    if len(request.seed_keywords) > 10:
        raise HTTPException(
            status_code=400,
            detail="You can specify a maximum of 10 seed keywords per discovery request."
        )
    
    async def run_discovery():
        # This function receives its own db session
        workflow_db = next(get_db())
        try:
            workflow = KeywordDiscoveryWorkflow(workflow_db)
            await workflow.discover_and_qualify_keywords(
                site_id=request.site_id,
                seed_keywords=request.seed_keywords,
                min_search_volume=request.min_search_volume,
                max_keyword_difficulty=request.max_keyword_difficulty,
                intent=request.intent,
                limit=request.limit
            )
        finally:
            workflow_db.close()
    
    background_tasks.add_task(run_discovery)
    
    return {
        "status": "started",
        "message": f"Discovering keywords for {len(request.seed_keywords)} seed keywords"
    }

@router.get("/site/{site_id}", response_model=List[KeywordResponse])
async def list_keywords(
    site_id: str,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List keywords for a site"""
    query = db.query(Keyword).filter_by(site_id=site_id)
    
    if status:
        query = query.filter_by(status=status)
    
    return query.order_by(Keyword.strategic_score.desc()).all()

# ADDED: New endpoint to list unclustered keywords
@router.get("/site/{site_id}/unclustered", response_model=List[KeywordResponse])
async def list_unclustered_keywords(site_id: str, db: Session = Depends(get_db)):
    """List keywords for a site that do not belong to any cluster."""
    # Query for keywords that are not linked to any cluster in the association table
    unclustered_keywords = (
        db.query(Keyword)
        .filter(Keyword.site_id == site_id)
        .filter(Keyword.status.in_(['qualified', 'completed', 'clustering'])) # MODIFIED: Include 'clustering' status for UI feedback
        .outerjoin(keyword_cluster_association)
        .filter(keyword_cluster_association.c.cluster_id == None)
        .order_by(Keyword.strategic_score.desc())
        .all()
    )
    return unclustered_keywords

@router.get("/{keyword_id}", response_model=KeywordResponse)
async def get_keyword(keyword_id: str, db: Session = Depends(get_db)):
    """Get keyword details with progress"""
    keyword = db.query(Keyword).filter_by(id=keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@router.delete("/{keyword_id}")
async def delete_keyword(keyword_id: str, db: Session = Depends(get_db)):
    """Delete a keyword"""
    keyword = db.query(Keyword).filter_by(id=keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    db.delete(keyword)
    db.commit()
    return {"message": "Keyword deleted successfully"}
```

#### **Granular Step II.C.2: Add Cluster Endpoints to `backend/app/api/sites.py`**

**Action:** Add endpoints to trigger clustering and list clusters.

**File:** `backend/app/api/sites.py`

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Site, KeywordCluster # MODIFIED: Added KeywordCluster
from app.schemas import SiteCreate, SiteResponse, KeywordClusterResponse # MODIFIED: Added KeywordClusterResponse
from typing import List
from app.workflows.keyword_clustering import KeywordClusteringWorkflow # MODIFIED: Import KeywordClusteringWorkflow

router = APIRouter(prefix="/api/sites", tags=["Sites"])

@router.post("/", response_model=SiteResponse)
async def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    """Create a new site"""
    db_site = Site(**site.dict())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/", response_model=List[SiteResponse])
async def list_sites(db: Session = Depends(get_db)):
    """List all sites"""
    return db.query(Site).filter_by(is_active=True).all()

@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(site_id: str, db: Session = Depends(get_db)):
    """Get site details"""
    site = db.query(Site).filter_by(id=site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

# ADDED: Endpoint to trigger keyword clustering for a site
@router.post("/{site_id}/trigger-clustering", response_model=dict)
async def trigger_keyword_clustering(
    site_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db) # Keep db session open only for validation
):
    """Trigger the AI-powered keyword clustering process for the site."""
    site = db.query(Site).filter_by(id=site_id, is_active=True).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    async def run_clustering():
        # Each background task gets its own DB session
        workflow_db = next(get_db())
        try:
            workflow = KeywordClusteringWorkflow(workflow_db)
            await workflow.cluster_and_save(site_id)
        finally:
            workflow_db.close()
    
    background_tasks.add_task(run_clustering)
    
    return {
        "status": "started",
        "message": f"Keyword clustering started for site: {site.name}"
    }

# ADDED: Endpoint to list keyword clusters for a site
@router.get("/{site_id}/clusters", response_model=List[KeywordClusterResponse])
async def list_clusters_for_site(site_id: str, db: Session = Depends(get_db)):
    """List all keyword clusters for a site, including their keywords."""
    clusters = (
        db.query(KeywordCluster)
        .filter(KeywordCluster.site_id == site_id)
        .options(joinedload(KeywordCluster.keywords).raiseload('*')) 
        .order_by(KeywordCluster.name)
        .all()
    )
    return clusters

@router.delete("/{site_id}")
async def delete_site(site_id: str, db: Session = Depends(get_db)):
    """Soft delete a site"""
    site = db.query(Site).filter_by(id=site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    site.is_active = False
    db.commit()
    return {"message": "Site deleted successfully"}
```

#### **Granular Step II.C.3: Add `generate_content_for_cluster` to `backend/app/api/content.py`**

**Action:** Add the endpoint to trigger batch content generation.

**File:** `backend/app/api/content.py`

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, engine # MODIFIED: Added 'engine'
from app.models import Content, Keyword, KeywordCluster # MODIFIED: Added KeywordCluster
from app.schemas import ContentGenerationRequest, ContentListResponse, FullContent
from app.workflows.content_generator import ContentGeneratorWorkflow
from app.workflows.publisher import PublisherWorkflow
from app.workflows.cluster_generator import ClusterGeneratorWorkflow # MODIFIED: Added ClusterGeneratorWorkflow
from typing import List

router = APIRouter(prefix="/api/content", tags=["Content"])

# ADDED: Endpoint to trigger batch content generation for a cluster
@router.post("/cluster/{cluster_id}/generate", response_model=dict)
async def generate_content_for_cluster(
    cluster_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db) # Keep this session open for initial validation/error handling if needed
):
    """Generate content for all qualified keywords in a cluster."""
    # Validate cluster existence
    cluster_check = db.query(KeywordCluster).filter_by(id=cluster_id).first()
    if not cluster_check:
        raise HTTPException(status_code=404, detail="Keyword Cluster not found")

    # Instantiate the workflow with the database engine and background tasks
    # The workflow itself will create new sessions for each individual content generation task
    workflow = ClusterGeneratorWorkflow(engine, background_tasks) 
    
    try:
        await workflow.generate_for_cluster(cluster_id)
        
        return {
            "status": "started",
            "message": f"Queued batch content generation for cluster {cluster_id}"
        }
    except Exception as e:
        # Catch budget exception or other major failures from the workflow
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate", response_model=dict)
async def generate_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate content for a keyword
    Runs complete pipeline in background
    """
    
    # Verify keyword exists and is qualified
    keyword = db.query(Keyword).filter_by(id=request.keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    # MODIFIED: Include 'clustering' in allowed statuses if it ever gets here, though unlikely
    if keyword.status not in ['qualified', 'completed', 'failed', 'clustering']:
        raise HTTPException(
            status_code=400,
            detail="Keyword must be qualified, completed, or failed before generating content"
        )
    
    async def run_generation():
        # This function receives its own db session
        workflow_db = next(get_db())
        try:
            workflow = ContentGeneratorWorkflow(workflow_db)
            await workflow.generate_complete_article(
                keyword_id=request.keyword_id,
                custom_prompt=request.custom_prompt
            )
        finally:
            workflow_db.close()
    
    background_tasks.add_task(run_generation)
    
    return {
        "status": "started",
        "message": f"Generating content for keyword: {keyword.keyword}"
    }

@router.post("/{content_id}/publish", response_model=dict)
async def publish_content(
    content_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Publish content to WordPress"""
    
    content = db.query(Content).filter_by(id=content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.status == 'published':
        raise HTTPException(status_code=400, detail="Content already published")
    
    async def run_publishing():
        # This function receives its own db session
        workflow_db = next(get_db())
        try:
            workflow = PublisherWorkflow(workflow_db)
            await workflow.publish_to_wordpress(content_id)
        finally:
            workflow_db.close()
    
    background_tasks.add_task(run_publishing)
    
    return {
        "status": "started",
        "message": "Publishing to WordPress"
    }

@router.get("/site/{site_id}", response_model=List[ContentListResponse])
async def list_content(
    site_id: str,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List content for a site"""
    query = db.query(Content).filter_by(site_id=site_id)
    
    if status:
        query = query.filter_by(status=status)
    
    return query.order_by(Content.created_at.desc()).all()

@router.get("/{content_id}", response_model=FullContent) # Now returns the full content body
async def get_content(content_id: str, db: Session = Depends(get_db)):
    """Get content details"""
    content = db.query(Content).filter_by(id=content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.put("/{content_id}")
async def update_content(
    content_id: str,
    title: str = None,
    body: str = None,
    meta_description: str = None,
    db: Session = Depends(get_db)
):
    """Update content before publishing"""
    content = db.query(Content).filter_by(id=content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if title:
        content.title = title
    if body:
        content.body = body
    if meta_description:
        content.meta_description = meta_description
    
    db.commit()
    return {"message": "Content updated successfully"}
```

#### **Granular Step II.C.4: Update `keyword_discovery.py` to Use Dedicated DB Session**

**Action:** Ensure `run_discovery` uses a dedicated DB session to avoid session-per-request issues with background tasks.

**File:** `backend/app/workflows/keyword_discovery.py`

```python
from sqlalchemy.orm import Session
from app.models import Keyword
from app.services.dataforseo import DataForSEOService
from app.services.cost_tracker import CostTracker
from app.workflows.filters import build_discovery_filters
from typing import List, Dict
import logging
from app.database import get_db # ADDED: Import get_db

logger = logging.getLogger(__name__)

class KeywordDiscoveryWorkflow:
    """
    Cost-optimized keyword discovery
    Estimated cost: ~$0.03 per seed keyword
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.cost_tracker = CostTracker(db)
        self.dataforseo = DataForSEOService(self.cost_tracker)
    
    async def discover_and_qualify_keywords(
        self,
        site_id: str,
        seed_keywords: List[str],
        min_search_volume: int = 500,
        max_keyword_difficulty: int = 20,
        intent: str = "informational",
        limit: int = 50
    ) -> List[Keyword]:
        """
        Discover keywords and automatically qualify them
        Returns only qualified keywords (meeting all criteria)
        """
        logger.info(f"Starting keyword discovery for site_id: {site_id} with {len(seed_keywords)} seed keywords.")
        
        config = {
            "min_search_volume": min_search_volume,
            "max_keyword_difficulty": max_keyword_difficulty,
            "allowed_intents": [intent] if intent else [],
            "enforce_intent_filter": True
        }
        std_api_filters, rel_api_filters = build_discovery_filters(config)
        
        estimated_cost = len(seed_keywords) * 0.03
        logger.info(f"Estimated cost for discovery: ${estimated_cost:.2f}")
        if not await self.cost_tracker.can_proceed(estimated_cost):
            logger.warning(f"Monthly budget exceeded. Cannot proceed with keyword discovery for site_id: {site_id}.")
            raise Exception("Monthly budget exceeded. Cannot proceed with keyword discovery.")
        
        discovered = await self.dataforseo.discover_keywords(
            seed_keywords=seed_keywords,
            filters=std_api_filters,
            related_filters=rel_api_filters
        )
        logger.info(f"Discovered {len(discovered)} potential keywords from DataForSEO.")

        # Check for existing keywords to prevent duplicates
        existing_keywords = {
            kw.keyword for kw in self.db.query(Keyword.keyword).filter(Keyword.site_id == site_id).all()
        }
        
        qualified_keywords = []
        for kw_data in discovered[:limit]:  # Limit to top N
            if kw_data.get("keyword") in existing_keywords:
                continue

            keyword_info = kw_data.get("keyword_info", {}) or {}
            keyword_props = kw_data.get("keyword_properties", {}) or {}
            search_intent = kw_data.get("search_intent_info", {}) or {}
            serp_info = kw_data.get("serp_info", {}) or {}
            
            keyword = Keyword(
                site_id=site_id,
                keyword=kw_data.get("keyword"),
                search_volume=keyword_info.get("search_volume"),
                keyword_difficulty=keyword_props.get("keyword_difficulty"),
                cpc=keyword_info.get("cpc"),
                competition_level=keyword_info.get("competition_level"),
                main_intent=search_intent.get("main_intent"),
                serp_features=serp_info.get("serp_item_types", []),
                strategic_score=kw_data.get("strategic_score"),
                status='qualified',
                discovery_cost=estimated_cost / len(discovered) if discovered else 0
            )
            
            self.db.add(keyword)
            qualified_keywords.append(keyword)
            existing_keywords.add(keyword.keyword) # Add to set to avoid duplicates in the same batch
        
        self.db.commit()
        logger.info(f"Saved {len(qualified_keywords)} new qualified keywords to the database.")
        
        return qualified_keywords
```

### **D) Frontend Implementation (Types, Services, State, Hooks, UI)**

#### **Granular Step II.D.1: Update Frontend Types (`frontend/src/types/index.ts`)**

**Action:** Add `KeywordCluster` and `TriggerClusteringRequest` interfaces.

**File:** `frontend/src/types/index.ts`

```typescript
export interface Site {
  id: string;
  name: string;
  domain: string;
  wordpress_url: string;
  is_active: boolean;
  created_at: string;
}

export interface Keyword {
  id: string;
  keyword: string;
  search_volume: number | null;
  keyword_difficulty: number | null;
  cpc: number | null;
  strategic_score: number | null;
  status: 'discovered' | 'qualified' | 'clustering' | 'analyzing' | 'generating' | 'completed' | 'failed'; // MODIFIED: Added 'clustering' status
  progress: number;
  error_message: string | null;
}

export interface Content {
  id: string;
  keyword_id: string;
  title: string | null;
  meta_description: string | null;
  status: 'draft' | 'published' | 'failed';
  wordpress_url: string | null;
  published_at: string | null;
}

export interface FullContent extends Content {
  body: string | null;
}

// ADDED: KeywordCluster interface
export interface KeywordCluster {
  id: string;
  name: string;
  keywords: Keyword[];
}

// ADDED: Interface for triggering clustering request
export interface TriggerClusteringRequest {
  site_id: string;
}

export interface CostAnalytics {
  total_spent: number;
  remaining_budget: number;
  avg_cost_per_article: number;
  articles_generated: number;
}

export interface DashboardStats {
  keywords: {
    total: number;
    qualified: number;
    processing: number;
  };
  content: {
    total: number;
    published: number;
    draft: number;
    recent_week: number;
  };
  costs: CostAnalytics;
}
```

#### **Granular Step II.D.2: Update Frontend API Service (`frontend/src/services/api.ts`)**

**Action:** Add new API methods for cluster listing, triggering, and batch generation, and for listing unclustered keywords.

**File:** `frontend/src/services/api.ts`

```typescript
import axios from 'axios';
import type { Site, Keyword, Content, DashboardStats, CostAnalytics, KeywordCluster, TriggerClusteringRequest } from '../types'; // MODIFIED: Added KeywordCluster, TriggerClusteringRequest

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Sites
export const sitesAPI = {
  create: (data: {
    name: string;
    domain: string;
    wordpress_url: string;
    wordpress_username: string;
    wordpress_app_password: string;
  }) => api.post<Site>('/api/sites/', data),
  
  list: () => api.get<Site[]>('/api/sites/'),
  
  get: (siteId: string) => api.get<Site>(`/api/sites/${siteId}`),
  
  delete: (siteId: string) => api.delete(`/api/sites/${siteId}`),

  // ADDED: New methods for clustering
  listClusters: (siteId: string) => api.get<KeywordCluster[]>(`/api/sites/${siteId}/clusters`),
  triggerClustering: (siteId: string) => api.post<TriggerClusteringRequest, any>(`/api/sites/${siteId}/trigger-clustering`),
};

// Keywords
export const keywordsAPI = {
  discover: (data: {
    site_id: string;
    seed_keywords: string[];
    min_search_volume?: number;
    max_keyword_difficulty?: number;
    intent?: string;
    limit?: number;
  }) => api.post('/api/keywords/discover', data),
  
  listBySite: (siteId: string, status?: string) => {
    const params = status ? { status } : {};
    return api.get<Keyword[]>(`/api/keywords/site/${siteId}`, { params });
  },

  // ADDED: New method to list unclustered keywords specifically
  listUnclustered: (siteId: string) => {
    return api.get<Keyword[]>(`/api/keywords/site/${siteId}/unclustered`);
  },
  
  get: (keywordId: string) => api.get<Keyword>(`/api/keywords/${keywordId}`),
  
  delete: (keywordId: string) => api.delete(`/api/keywords/${keywordId}`),
};

// Content
export const contentAPI = {
  generate: (data: {
    keyword_id: string;
    custom_prompt?: string;
  }) => api.post('/api/content/generate', data),
  
  // ADDED: New method for batch content generation for a cluster
  generateCluster: (clusterId: string) => 
    api.post(`/api/content/cluster/${clusterId}/generate`),
  
  publish: (contentId: string) => 
    api.post(`/api/content/${contentId}/publish`),
  
  listBySite: (siteId: string, status?: string) => {
    const params = status ? { status } : {};
    return api.get<Content[]>(`/api/content/site/${siteId}`, { params });
  },
  
  get: (contentId: string) => api.get<Content>(`/api/content/${contentId}`),
  
  update: (contentId: string, data: {
    title?: string;
    body?: string;
    meta_description?: string;
  }) => api.put(`/api/content/${contentId}`, data),
};

// Analytics
export const analyticsAPI = {
  getCosts: () => api.get<CostAnalytics>('/api/analytics/costs'),
  
  getDashboard: () => api.get<DashboardStats>('/api/analytics/dashboard'),
};

export default api;
```

#### **Granular Step II.D.3: Update Frontend State Management (`frontend/src/store/useStore.ts`)**

**Action:** Add `keywordClusters` state and `setKeywordClusters` action.

**File:** `frontend/src/store/useStore.ts`

```typescript
import { create } from 'zustand';
import type { Site, Keyword, Content, KeywordCluster } from '../types'; # MODIFIED: Added KeywordCluster

interface AppState {
  # Sites
  sites: Site[];
  selectedSite: Site | null;
  setSites: (sites: Site[]) => void;
  setSelectedSite: (site: Site | null) => void;
  
  # Keywords
  keywords: Keyword[];
  keywordClusters: KeywordCluster[]; # MODIFIED: Added keywordClusters
  setKeywords: (keywords: Keyword[]) => void;
  setKeywordClusters: (clusters: KeywordCluster[]) => void; # MODIFIED: Added setKeywordClusters
  updateKeyword: (keywordId: string, updates: Partial<Keyword>) => void;
  
  # Content
  content: Content[];
  setContent: (content: Content[]) => void;
  
  # UI State
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useStore = create<AppState>((set) => ({
  # Sites
  sites: [],
  selectedSite: null,
  setSites: (sites) => set({ sites }),
  setSelectedSite: (site) => set({ selectedSite: site }),
  
  # Keywords
  keywords: [],
  keywordClusters: [], # MODIFIED: Initial state for keywordClusters
  setKeywords: (keywords) => set({ keywords }),
  setKeywordClusters: (clusters) => set({ keywordClusters: clusters }), # MODIFIED: Action to set keywordClusters
  updateKeyword: (keywordId, updates) =>
    set((state) => ({
      keywords: state.keywords.map((kw) =>
        kw.id === keywordId ? { ...kw, ...updates } : kw
      ),
    })),
  
  # Content
  content: [],
  setContent: (content) => set({ content }),
  
  # UI State
  isLoading: false,
  setIsLoading: (isLoading) => set({ isLoading }),
}));
```

#### **Granular Step II.D.4: Update Frontend Keywords Hook (`frontend/src/hooks/useKeywords.ts`)**

**Action:** Refactor the `useKeywords` hook to fetch both all keywords (for general status updates) and a dedicated list of unclustered keywords (for performance on the Keywords page).

**File:** `frontend/src/hooks/useKeywords.ts`

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { keywordsAPI } from '../services/api';
import { useStore } from '../store/useStore';
import { useEffect } from 'react';
import { Keyword } from '../types';

export function useKeywords(siteId: string | null) {
  const queryClient = useQueryClient();
  const { keywords, setKeywords } = useStore();

  // Query to fetch ALL keywords (primarily for showing processing status across the whole list, e.g., in dashboard)
  // This query will also automatically refresh when any other keyword-related query is invalidated.
  const { data: allKeywords, isLoading: isAllKeywordsLoading, error: allKeywordsError } = useQuery<Keyword[], Error>({
    queryKey: ['keywords', siteId],
    queryFn: () => (siteId ? keywordsAPI.listBySite(siteId).then(res => res.data) : Promise.resolve([])),
    enabled: !!siteId,
    refetchInterval: 5000, // Poll to update progress bars/statuses
  });

  // Query to fetch UNCLUSTERED keywords specifically (optimized for display on KeywordsPage)
  // This query will also automatically refresh when other keyword-related queries are invalidated.
  const { data: unclusteredKeywordsData, isLoading: isUnclusteredKeywordsLoading, error: unclusteredKeywordsError } = useQuery<Keyword[], Error>({
    queryKey: ['keywords-unclustered', siteId],
    queryFn: () => (siteId ? keywordsAPI.listUnclustered(siteId).then(res => res.data) : Promise.resolve([])),
    enabled: !!siteId,
    refetchInterval: 5000, // Poll to update progress bars/statuses
  });

  // Effect to update the global store with ALL keywords
  useEffect(() => {
    if (allKeywords) {
      setKeywords(allKeywords);
    }
  }, [allKeywords, setKeywords]);

  const discoverKeywordsMutation = useMutation({
    mutationFn: keywordsAPI.discover,
    onSuccess: () => {
      // Invalidate all relevant queries to ensure data freshness across the app
      queryClient.invalidateQueries({ queryKey: ['keywords', siteId] });
      queryClient.invalidateQueries({ queryKey: ['keywords-unclustered', siteId] });
      queryClient.invalidateQueries({ queryKey: ['keywordClusters', siteId] });
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || 'An unexpected error occurred.';
      alert(`Discovery Failed: ${errorMessage}`);
    },
  });

  const deleteKeywordMutation = useMutation({
    mutationFn: keywordsAPI.delete,
    onSuccess: () => {
      // Invalidate all relevant queries after a deletion
      queryClient.invalidateQueries({ queryKey: ['keywords', siteId] });
      queryClient.invalidateQueries({ queryKey: ['keywords-unclustered', siteId] });
      queryClient.invalidateQueries({ queryKey: ['keywordClusters', siteId] });
    },
  });

  return {
    keywords: allKeywords || [], // Exports all keywords (for dashboards, etc.)
    unclusteredKeywords: unclusteredKeywordsData || [], // Exports only unclustered keywords for the specific UI section
    isLoading: isAllKeywordsLoading || isUnclusteredKeywordsLoading,
    error: allKeywordsError || unclusteredKeywordsError,
    discoverKeywords: discoverKeywordsMutation.mutate,
    isDiscovering: discoverKeywordsMutation.isPending,
    deleteKeyword: deleteKeywordMutation.mutate,
  };
}
```

#### **Granular Step II.D.5: Create `useClusterManager` Hook (`frontend/src/hooks/useClusterManager.ts`)**

**Action:** Create a custom hook to centralize all clustering and batch generation logic for the frontend.

**File:** `frontend/src/hooks/useClusterManager.ts`

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { sitesAPI, contentAPI } from '../services/api';
import { useStore } from '../store/useStore';
import { useEffect } from 'react';
import { toast } from 'react-hot-toast'; // ADDED: For professional notifications

export function useClusterManager(siteId: string | null) {
    const queryClient = useQueryClient();
    const { setKeywordClusters } = useStore();

    // Query to fetch all keyword clusters for the selected site
    const { data: clusters, isLoading: isLoadingClusters } = useQuery({
        queryKey: ['keywordClusters', siteId],
        queryFn: () => siteId ? sitesAPI.listClusters(siteId).then(res => res.data) : Promise.resolve([]),
        enabled: !!siteId,
        refetchInterval: 10000, // Poll to keep clusters updated (e.g., if new ones are created by another user/process)
    });

    // Effect to update the global store with the fetched clusters
    useEffect(() => {
        if (clusters) {
            setKeywordClusters(clusters);
        }
    }, [clusters, setKeywordClusters]);
    
    // Mutation to trigger the AI clustering process
    const triggerClusteringMutation = useMutation({
        mutationFn: sitesAPI.triggerClustering,
        onSuccess: () => {
            toast.success("AI Clustering started! Your keyword lists will update automatically as keywords are processed.");
            // Invalidate queries to refresh the keyword and cluster lists
            queryClient.invalidateQueries({ queryKey: ['keywordClusters', siteId] });
            queryClient.invalidateQueries({ queryKey: ['keywords-unclustered', siteId] });
            queryClient.invalidateQueries({ queryKey: ['keywords', siteId] }); // Invalidate all keywords to update status like 'clustering'
        },
        onError: (error: any) => {
            toast.error(`Clustering failed: ${error.response?.data?.detail || 'An unexpected error occurred.'}`);
            // Also invalidate on error to revert any 'clustering' statuses
            queryClient.invalidateQueries({ queryKey: ['keywords-unclustered', siteId] });
            queryClient.invalidateQueries({ queryKey: ['keywords', siteId] });
        }
    });

    // Mutation to trigger batch content generation for an entire cluster
    const generateClusterMutation = useMutation({
        mutationFn: contentAPI.generateCluster,
        onSuccess: (_, clusterId) => {
            toast.success(`Batch content generation started for the cluster. New content drafts will appear on the Content page.`);
            // Invalidate queries to update keyword statuses (e.g., from 'qualified' to 'generating')
            // and to show new content items
            queryClient.invalidateQueries({ queryKey: ['keywordClusters', siteId] });
            queryClient.invalidateQueries({ queryKey: ['keywords', siteId] });
            queryClient.invalidateQueries({ queryKey: ['content', siteId] });
        },
        onError: (error: any) => {
            toast.error(`Batch Generation Failed: ${error.response?.data?.detail || 'An unexpected error occurred.'}`);
            // Invalidate on error to revert keyword statuses if needed
            queryClient.invalidateQueries({ queryKey: ['keywords', siteId] });
        }
    });

    return {
        clusters: clusters || [],
        isLoadingClusters,
        triggerClustering: triggerClusteringMutation.mutate,
        isClustering: triggerClusteringMutation.isPending,
        generateClusterContent: generateClusterMutation.mutate,
        isGeneratingCluster: generateClusterMutation.isPending
    };
}
```

#### **Granular Step II.D.6: Update `KeywordList` Component (`frontend/src/components/keywords/KeywordList.tsx`)**

**Action:** Add `isNested` and `title` props for flexible rendering within cluster cards and for the unclustered section. Update status badge styles for 'clustering'.

**File:** `frontend/src/components/keywords/KeywordList.tsx`

```typescript
import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { ProgressBar } from '../common/ProgressBar';
import { Trash2, Play } from 'lucide-react';
import type { Keyword } from '../../types';
import { useContent } from '../../hooks/useContent';
import { useStore } from '../../store/useStore';

interface KeywordListProps {
  keywords: Keyword[];
  onDelete: (id: string) => void;
  isNested?: boolean; // ADDED: New prop for nested rendering
  title?: string;     // ADDED: New prop for custom title
}

export function KeywordList({ keywords, onDelete, isNested = false, title }: KeywordListProps) {
  const { selectedSite } = useStore();
  const { generateContent, isGenerating } = useContent(selectedSite?.id || null);

  const getStatusBadge = (status: string) => {
    const styles = {
      discovered: 'bg-gray-100 text-gray-800',
      qualified: 'bg-green-100 text-green-800',
      clustering: 'bg-indigo-100 text-indigo-800 animate-pulse', // MODIFIED: New style for 'clustering'
      analyzing: 'bg-yellow-100 text-yellow-800',
      generating: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    };

    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${styles[status as keyof typeof styles]}`}>
        {status}
      </span>
    );
  };

  // The table structure extracted into a reusable fragment
  const tableContent = (
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-3 px-4">Keyword</th>
              <th className="text-left py-3 px-4">Volume</th>
              <th className="text-left py-3 px-4">Difficulty</th>
              <th className="text-left py-3 px-4">Score</th>
              <th className="text-left py-3 px-4">Status</th>
              <th className="text-left py-3 px-4">Progress</th>
              <th className="text-right py-3 px-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {keywords.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-gray-500">
                  No keywords found. Discover some keywords to get started.
                </td>
              </tr>
            ) : (
              keywords.map((keyword) => (
                <tr key={keyword.id} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{keyword.keyword}</td>
                  <td className="py-3 px-4">{keyword.search_volume?.toLocaleString() || 'N/A'}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs ${
                      (keyword.keyword_difficulty || 0) <= 20 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {keyword.keyword_difficulty || 'N/A'}
                    </span>
                  </td>
                  <td className="py-3 px-4">{keyword.strategic_score?.toFixed(1) || 'N/A'}</td>
                  <td className="py-3 px-4">
                    <div className="relative group">
                      {getStatusBadge(keyword.status)}
                      {keyword.status === 'failed' && keyword.error_message && (
                        <div className="absolute bottom-full mb-2 w-64 bg-gray-800 text-white text-xs rounded py-2 px-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
                          {keyword.error_message}
                        </div>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    {keyword.progress > 0 && keyword.progress < 100 ? (
                      <ProgressBar progress={keyword.progress} />
                    ) : (
                      <span className="text-sm text-gray-500">
                        {keyword.progress === 100 ? 'Complete' : '-'}
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex justify-end gap-2">
                      {/* MODIFIED: Disable generation if keyword is 'clustering' */}
                      {keyword.status === 'qualified' && (
                        <Button
                          onClick={() => generateContent({ keyword_id: keyword.id })}
                          disabled={isGenerating}
                        >
                          <Play size={16} />
                        </Button>
                      )}
                      {/* MODIFIED: Disable delete if keyword is 'clustering' */}
                      <Button
                        variant="danger"
                        onClick={() => {
                          if (confirm('Delete this keyword?')) {
                            onDelete(keyword.id);
                          }
                        }}
                        disabled={keyword.status === 'clustering'}
                        title={keyword.status === 'clustering' ? "Cannot delete keywords while clustering" : "Delete keyword"}
                      >
                        <Trash2 size={16} />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
  );

  return isNested ? ( // MODIFIED: Conditional render based on `isNested`
      tableContent 
    ) : (
      <Card title={title || `Keywords (${keywords.length})`}> {/* MODIFIED: Use `title` prop */}
        {tableContent}
      </Card>
    );
}
```

#### **Granular Step II.D.7: Create `KeywordClusterCard` Component (`frontend/src/components/keywords/KeywordClusterCard.tsx`)**

**Action:** Create a new component to display a single keyword cluster with its keywords and batch actions.

**File:** `frontend/src/components/keywords/KeywordClusterCard.tsx`

```typescript
import React from 'react';
import type { KeywordCluster } from '../../types';
import { KeywordList } from './KeywordList';
import { Button } from '../common/Button';
import { FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { useClusterManager } from '../../hooks/useClusterManager';

interface KeywordClusterCardProps {
  cluster: KeywordCluster;
  onDeleteKeyword: (id: string) => void;
}

export function KeywordClusterCard({ cluster, onDeleteKeyword }: KeywordClusterCardProps) {
  const [isOpen, setIsOpen] = React.useState(true);
  const { selectedSite } = useStore();
  const { generateClusterContent, isGeneratingCluster } = useClusterManager(selectedSite?.id || null);
  
  const qualifiedKeywordsCount = cluster.keywords.filter(k => k.status === 'qualified').length;
  const isButtonDisabled = isGeneratingCluster || qualifiedKeywordsCount === 0;

  const handleGenerateForCluster = () => {
    if (qualifiedKeywordsCount > 0 && selectedSite) {
        generateClusterContent(cluster.id);
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md mb-6">
      <div className="p-4 border-b flex justify-between items-center cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <div className="flex items-center gap-3">
            {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
            <h3 className="text-xl font-bold">{cluster.name}</h3>
            <span className="text-sm text-gray-500">({cluster.keywords.length} Keywords)</span>
        </div>
        <Button 
            onClick={e => { e.stopPropagation(); handleGenerateForCluster(); }} 
            variant="secondary"
            disabled={isButtonDisabled}
            isLoading={isGeneratingCluster}
            title={qualifiedKeywordsCount === 0 ? "No qualified keywords in this cluster to generate content for." : `Generate content for all ${qualifiedKeywordsCount} qualified keywords in this cluster.`}
        >
          <FileText size={16} className="mr-2" />
          {isGeneratingCluster ? 'Queuing...' : `Generate All (${qualifiedKeywordsCount})`}
        </Button>
      </div>
      
      {isOpen && (
        <div className="p-4">
            <KeywordList keywords={cluster.keywords} onDelete={onDeleteKeyword} isNested={true} />
        </div>
      )}
    </div>
  );
}
```

#### **Granular Step II.D.8: Refactor `KeywordsPage.tsx` to Display Clusters and Unclustered Keywords (`frontend/src/pages/KeywordsPage.tsx`)**

**Action:** Update the page logic to fetch and display clustered and unclustered keywords using the new hooks and components, including the "Trigger AI Clustering" button.

**File:** `frontend/src/pages/KeywordsPage.tsx`

```typescript
import React from 'react';
import { useStore } from '../store/useStore';
import { useQuery } from '@tanstack/react-query';
import { analyticsAPI } from '../services/api';
import { useKeywords } from '../hooks/useKeywords';
import { useClusterManager } from '../hooks/useClusterManager';
import { KeywordDiscoveryForm } from '../components/keywords/KeywordDiscoveryForm';
import { KeywordClusterCard } from '../components/keywords/KeywordClusterCard';
import { KeywordList } from '../components/keywords/KeywordList';
import { Button } from '../components/common/Button';

export function KeywordsPage() {
  const { selectedSite } = useStore();
  const siteId = selectedSite?.id || null;

  // Use useKeywords for unclustered keywords and deletion
  const { unclusteredKeywords, isLoading: isLoadingKeywords, error: keywordsError, deleteKeyword } = useKeywords(siteId);
  
  // Use useClusterManager for clusters and clustering actions
  const { clusters, isLoadingClusters, triggerClustering, isClustering } = useClusterManager(siteId);
  
  // Fetch cost analytics for budget estimation
  const { data: costAnalytics } = useQuery({
    queryKey: ['costs'],
    queryFn: () => analyticsAPI.getCosts().then(res => res.data),
    enabled: !!siteId,
    refetchInterval: 30000, // Poll for budget updates
  });

  if (!selectedSite) {
    return <div className="text-center py-12 text-gray-500">Please select a site to continue.</div>;
  }

  const isLoading = isLoadingKeywords || isLoadingClusters;
  if (isLoading) return <div>Loading keywords and clusters...</div>;
  if (keywordsError) return <div>Error loading keywords: {keywordsError.message}</div>;

  const hasUnclustered = unclusteredKeywords.length > 0;
  // Simplified fixed cost for the AI clustering API call (adjust based on actual token usage)
  const estimatedClusteringCost = hasUnclustered ? 0.05 : 0; 
  const canCluster = costAnalytics ? costAnalytics.remaining_budget >= estimatedClusteringCost : true;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Keywords for {selectedSite.name}</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-1">
          <KeywordDiscoveryForm siteId={selectedSite.id} />
        </div>
        
        <div className="lg:col-span-2 flex flex-col justify-start items-end">
            {hasUnclustered && (
                <>
                    <Button 
                        onClick={() => triggerClustering(siteId!)} 
                        isLoading={isClustering}
                        disabled={!canCluster || isClustering}
                        className="h-10"
                        title={
                            !hasUnclustered 
                                ? "No new keywords to cluster" 
                                : (!canCluster ? `Not enough budget ($${costAnalytics?.remaining_budget.toFixed(2)} remaining, $${estimatedClusteringCost.toFixed(2)} needed)` : "Group unclustered keywords into topics for better organization")
                        }
                    >
                        {isClustering ? 'Clustering...' : `Trigger AI Clustering (${unclusteredKeywords.length} New)`}
                    </Button>
                    {hasUnclustered && costAnalytics && (
                        <p className="text-xs mt-2">
                            <span className={!canCluster ? "text-red-500 font-bold" : "text-gray-600"}>
                                Est. Clustering Cost: ${estimatedClusteringCost.toFixed(2)}
                            </span>
                            <span className="mx-1">|</span>
                            <span className={!canCluster ? "text-red-500 font-bold" : "text-gray-600"}>
                                Remaining Budget: ${costAnalytics.remaining_budget.toFixed(2)}
                            </span>
                        </p>
                    )}
                </>
            )}
        </div>
      </div>
      
      {clusters.length === 0 && !hasUnclustered && (
        <div className="text-center py-12 text-gray-500 bg-white rounded-lg shadow-md">
            No qualified keywords yet. Discover some keywords using the form above to begin populating clusters.
        </div>
      )}

      {/* Render Clustered Keywords */}
      {clusters.map(cluster => (
        <KeywordClusterCard 
            key={cluster.id} 
            cluster={cluster} 
            onDeleteKeyword={deleteKeyword} 
        />
      ))}

      {/* Render Unclustered Keywords */}
      {hasUnclustered && (
         <div className="mt-8">
             <KeywordList 
                keywords={unclusteredKeywords} 
                onDelete={deleteKeyword} 
                title={`Unclustered Keywords (${unclusteredKeywords.length})`}
             />
         </div>
      )}
    </div>
  );
}
```

#### **Granular Step II.D.9: Update `App.tsx` with Toast Provider (`frontend/src/App.tsx`)**

**Action:** Integrate `react-hot-toast` for professional, non-blocking notifications.

**File:** `frontend/src/App.tsx`

```typescript
import { Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { KeywordsPage } from './pages/KeywordsPage';
import { ContentPage } from './pages/ContentPage';
import { SettingsPage } from './pages/SettingsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import { Toaster } from 'react-hot-toast'; # ADDED: Import Toaster

function App() {
  return (
    <Layout>
      <Toaster position="top-right" /> # ADDED: Toaster component for global notifications
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/keywords" element={<KeywordsPage />} />
        <Route path="/content" element={<ContentPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
```