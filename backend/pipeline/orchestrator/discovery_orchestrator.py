# backend/pipeline/orchestrator/discovery_orchestrator.py
import logging
import traceback
import os
from typing import Dict, Any, List, Optional

from backend.services.serp_analysis_service import SerpAnalysisService

logger = logging.getLogger(__name__)


class DiscoveryOrchestrator:
    def _run_discovery_background(
        self,
        job_id: str,
        run_id: int,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        disqualification_rules_override: Optional[Dict[str, Any]],
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = None,
        include_clickstream_data: Optional[bool] = None,
        closely_variants: Optional[bool] = None,
        exact_match: Optional[bool] = None,
        negative_keywords: Optional[List[str]] = None,
    ):
        """Internal method to execute the consolidated discovery phase for a job."""
        log_dir = "discovery_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"run_{run_id}.log")

        run_logger = logging.getLogger(f"run_{run_id}")
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        run_logger.addHandler(handler)
        run_logger.setLevel(logging.INFO)

        self.db_manager.update_discovery_run_log_path(run_id, log_file_path)
        self.db_manager.update_discovery_run_status(run_id, "running")
        self.job_manager.update_job_status(job_id, "running", progress=0)

        run_config = self.global_cfg_manager.load_client_config(
            self.client_id, self.db_manager
        )
        if disqualification_rules_override:
            run_logger.info(f"Applying disqualification rule overrides: {disqualification_rules_override}")
            run_config.update(disqualification_rules_override)

        run_logger.info(
            f"Starting discovery with modes: {discovery_modes}, filters: {filters}, order_by: {order_by}, limit: {limit}, depth: {depth}"
        )

        try:
            job_status = self.job_manager.get_job_status(job_id)
            if job_status and job_status.get("status") == "failed":
                run_logger.warning(
                    "Job found marked as 'failed' (cancelled). Exiting gracefully."
                )
                self.db_manager.update_discovery_run_status(run_id, "cancelled")
                return {"message": "Job cancelled by user request."}

            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=10,
                result={"step": "Fetching & Scoring keywords"},
            )

            from pipeline.step_01_discovery.run_discovery import run_discovery_phase

            discovery_result = run_discovery_phase(
                seed_keywords=seed_keywords,
                dataforseo_client=self.dataforseo_client,
                db_manager=self.db_manager,
                client_id=self.client_id,
                client_cfg=run_config,
                discovery_modes=discovery_modes,
                filters=filters,
                order_by=order_by,
                limit=limit,
                depth=depth,
                ignore_synonyms=ignore_synonyms,
                include_clickstream_data=include_clickstream_data,
                closely_variants=closely_variants,
                negative_keywords=negative_keywords,
                run_logger=run_logger,
            )

            stats = discovery_result.get("stats", {})
            total_cost = discovery_result.get("total_cost", 0.0)
            processed_opportunities = discovery_result.get("opportunities", [])

            self.job_manager.update_job_status(
                job_id, "running", progress=75, result={"step": "Saving to Database"}
            )

            num_added = 0
            if processed_opportunities:
                run_logger.info(
                    f"Attempting to save {len(processed_opportunities)} processed opportunities..."
                )
                num_added = self.db_manager.add_opportunities(
                    processed_opportunities, self.client_id, run_id
                )
                run_logger.info(
                    f"Successfully saved {num_added} new keyword records. The database ignored {len(processed_opportunities) - num_added} duplicates."
                )

            results_summary = {
                "total_cost": total_cost,
                "source_counts": stats.get("raw_counts", {}),
                "total_raw_count": stats.get("total_raw_count", 0),
                "total_unique_count": stats.get("total_unique_count", 0),
                "disqualification_reasons": stats.get("disqualification_reasons", {}),
                "disqualified_count": stats.get("disqualified_count", 0),
                "final_qualified_count": stats.get("final_qualified_count", 0),
                "duplicates_removed": len(processed_opportunities) - num_added,
                "final_added_to_db": num_added,
            }

            self.db_manager.update_discovery_run_completed(run_id, results_summary)
            self.job_manager.update_job_status(
                job_id, "completed", progress=100, result=results_summary
            )
            run_logger.info("Discovery run completed successfully.")
            return results_summary
        except Exception as e:
            error_message = f"Discovery workflow failed: {e}\n{traceback.format_exc()}"
            run_logger.error(error_message)
            self.db_manager.update_discovery_run_failed(run_id, str(e))
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise

    def run_discovery_and_save(
        self,
        run_id: int,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]] = None,
        order_by: Optional[List[str]] = None,
        disqualification_rules_override: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = None,
        include_clickstream_data: Optional[bool] = None,
        closely_variants: Optional[bool] = None,
        exact_match: Optional[bool] = None,
        negative_keywords: Optional[List[str]] = None,
    ) -> str:
        """
        Public method to initiate a discovery run asynchronously.
        Returns a job_id.
        """
        self.logger.info(
            f"--- Orchestrator: Initiating Full Discovery & Qualification for Run ID: {run_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_discovery_background,
            args=(
                run_id,
                seed_keywords,
                discovery_modes,
                filters,
                order_by,
                disqualification_rules_override,
                limit,
                depth,
                ignore_synonyms,
                include_clickstream_data,
                closely_variants,
                exact_match,
                negative_keywords,
            ),
        )
        return job_id
