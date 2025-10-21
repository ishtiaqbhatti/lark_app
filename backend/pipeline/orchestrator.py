# backend/pipeline/orchestrator.py
import logging

from app_config.manager import ConfigManager
from data_access.database_manager import DatabaseManager
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from external_apis.openai_client import OpenAIClientWrapper
from agents.image_generator import ImageGenerator
from agents.social_media_crafter import SocialMediaCrafter
from agents.internal_linking_suggester import InternalLinkingSuggester
from agents.html_formatter import HtmlFormatter
from core.blueprint_factory import BlueprintFactory
from agents.content_auditor import ContentAuditor
from agents.prompt_assembler import DynamicPromptAssembler
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine
from pipeline.step_01_discovery.cannibalization_checker import (
    CannibalizationChecker,
)
from jobs import JobManager

from .orchestrator.discovery_orchestrator import DiscoveryOrchestrator
from .orchestrator.analysis_orchestrator import AnalysisOrchestrator
from .orchestrator.content_orchestrator import ContentOrchestrator
from .orchestrator.image_orchestrator import ImageOrchestrator
from .orchestrator.social_orchestrator import SocialOrchestrator
from .orchestrator.validation_orchestrator import ValidationOrchestrator
from .orchestrator.workflow_orchestrator import WorkflowOrchestrator
from .orchestrator.cost_estimator import CostEstimator

logger = logging.getLogger(__name__)


class WorkflowOrchestrator(
    DiscoveryOrchestrator,
    AnalysisOrchestrator,
    ContentOrchestrator,
    ImageOrchestrator,
    SocialOrchestrator,
    ValidationOrchestrator,
    WorkflowOrchestrator,
    CostEstimator,
):
    def __init__(
        self,
        global_cfg_manager: ConfigManager,
        db_manager: DatabaseManager,
        client_id: str,
        job_manager: "JobManager",
    ):
        self.global_cfg_manager = global_cfg_manager
        self.db_manager = db_manager
        self.client_id = client_id
        self.job_manager = job_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client_cfg = self.global_cfg_manager.load_client_config(
            self.client_id, self.db_manager
        )

        self.openai_client = OpenAIClientWrapper(
            api_key=self.client_cfg.get("openai_api_key"), client_cfg=self.client_cfg
        )
        self.dataforseo_client = DataForSEOClientV2(
            login=self.client_cfg["dataforseo_login"],
            password=self.client_cfg["dataforseo_password"],
            config=self.client_cfg,
            db_manager=self.db_manager,
            enable_cache=self.client_cfg.get("enable_cache", True),
        )

        self.image_generator = ImageGenerator(self.client_cfg)
        self.social_crafter = SocialMediaCrafter(self.openai_client, self.client_cfg)
        self.internal_linking_suggester = InternalLinkingSuggester(
            self.openai_client, self.client_cfg, self.db_manager
        )
        self.html_formatter = HtmlFormatter()
        self.blueprint_factory = BlueprintFactory(
            self.openai_client, self.client_cfg, self.dataforseo_client, self.db_manager
        )
        self.scoring_engine = ScoringEngine(self.client_cfg)
        self.cannibalization_checker = CannibalizationChecker(
            self.client_cfg.get("target_domain"),
            self.dataforseo_client,
            self.client_cfg,
            self.db_manager,
        )
        self.content_auditor = ContentAuditor()
        self.prompt_assembler = DynamicPromptAssembler(self.db_manager)
