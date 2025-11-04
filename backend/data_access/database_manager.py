import sqlite3
import json
import threading
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import logging
import bleach  # ADD THIS LINE
import os
from . import queries
from backend.app_config.manager import ConfigManager

ALLOWED_ATTRIBUTES_DB = {
    "*": ["id", "class"],
    "a": ["href", "title"],
    "img": ["src", "alt", "width", "height"],
}

# W20 FIX: Define sanitization constants globally or as module constants (based on router update logic)
ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "br",
    "a",
    "i",
    "u",
    "em",
    "strong",
    "blockquote",
    "li",
    "ul",
    "ol",
    "img",
    "div",
    "span",
    "table",
    "thead",
    "tbody",
    "tr",
    "td",
    "th",
    "code",
    "pre",
]
ALLOWED_ATTRIBUTES = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()
ALLOWED_ATTRIBUTES.update(
    {
        "a": ["href", "title"],
        "img": ["src", "alt", "width", "height", "style"],
        "*": ["id", "class", "style"],
    }
)

DB_FILE = "data/opportunities.db"


class DatabaseManager:
    """Handles all interactions with the SQLite opportunity queue database."""

    def __init__(
        self, cfg_manager: Optional[ConfigManager] = None, db_path: Optional[str] = None
    ):  # db_path is now passed via cfg_manager
        self.cfg_manager = cfg_manager

        # Define project root relative to this file's location
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        if db_path:
            self.db_path = db_path
            self.db_type = "sqlite"
        elif cfg_manager:
            global_cfg = cfg_manager.get_global_config()
            db_file_name = global_cfg.get("db_file_name", DB_FILE)
            self.db_path = os.path.join(
                project_root, db_file_name
            )  # Ensure path is relative to project root
            self.db_type = global_cfg.get("db_type", "sqlite")
        else:
            db_file_name = DB_FILE
            self.db_path = os.path.join(
                project_root, db_file_name
            )  # Ensure path is relative to project root
            self.db_type = "sqlite"

        self.logger = logging.getLogger(self.__class__.__name__)
        self._thread_local = threading.local()

    def initialize(self):
        """Connects to the DB, creates tables, applies migrations, and ensures default client exists."""
        conn = self._get_conn()
        try:
            # Combine all CREATE TABLE statements into a single script for atomic execution
            full_schema_script = f"""
                {queries.CREATE_OPPORTUNITIES_TABLE}
                {queries.CREATE_CLIENTS_TABLE}
                {queries.CREATE_CLIENT_SETTINGS_TABLE}
                {queries.CREATE_DISCOVERY_RUNS_TABLE}
                {queries.CREATE_SCHEMA_VERSION_TABLE}
                {queries.CREATE_JOBS_TABLE}
                {queries.CREATE_CONTENT_HISTORY_TABLE}
                {queries.CREATE_CONTENT_FEEDBACK_TABLE}
                {queries.CREATE_API_CACHE_TABLE}
            """
            with conn:  # Ensure transaction for initial setup
                conn.executescript(full_schema_script)

            self._apply_migrations_from_files()
            self._ensure_default_client_exists(conn)
            
            # --- ADD THIS LINE ---
            self.clear_api_cache()
            
            self.logger.info("Database initialized.")
        finally:
            self._close_conn()

    def _get_conn(self):
        """Gets a connection from the thread-local storage or creates a new one."""
        if not hasattr(self._thread_local, "conn") or self._thread_local.conn is None:
            if self.db_type == "sqlite":
                self._thread_local.conn = sqlite3.connect(
                    self.db_path, check_same_thread=False
                )
                self._thread_local.conn.row_factory = sqlite3.Row
            else:
                raise NotImplementedError(
                    f"External database type '{self.db_type}' is not yet implemented."
                )
        return self._thread_local.conn

    def _close_conn(self):
        """Closes the connection for the current thread."""
        if hasattr(self._thread_local, "conn") and self._thread_local.conn is not None:
            self._thread_local.conn.close()
            self._thread_local.conn = None

    def _ensure_default_client_exists(self, conn):
        """Checks for and creates the default client if it doesn't exist in the database."""
        if not self.cfg_manager:
            return

        global_cfg = self.cfg_manager.get_global_config()
        default_id = global_cfg.get("default_client_id")

        if not default_id:
            self.logger.warning("No default_client_id found in configuration.")
            return

        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT 1 FROM clients WHERE client_id = ?", (default_id,)
        )
        if cursor.fetchone() is None:
            self.logger.warning(
                f"Default client '{default_id}' not found in database. Creating it now."
            )
            default_settings_template = (
                self.cfg_manager.get_default_client_settings_template()
            )
            self.add_client(default_id, default_id, default_settings_template)

    def _get_current_schema_version(self, conn) -> int:
        """Retrieves the current schema version from the database."""
        cursor = conn.execute(queries.GET_SCHEMA_VERSION)
        result = cursor.fetchone()
        return result["version"] if result else 0

    def _apply_migrations_from_files(self):
        """Applies SQL migration scripts from the migrations directory."""
        conn = self._get_conn()
        try:
            current_version = self._get_current_schema_version(conn)
            migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")

            if not os.path.exists(migrations_dir):
                self.logger.warning(
                    f"Migrations directory not found: {migrations_dir}. Skipping migrations."
                )
                return

            migration_files = sorted(
                [f for f in os.listdir(migrations_dir) if f.endswith(".sql")]
            )

            for filename in migration_files:
                version_str = filename.split("_")[0]
                if not version_str.isdigit():
                    self.logger.warning(
                        f"Skipping malformed migration file: {filename}"
                    )
                    continue

                version = int(version_str)

                if version > current_version:
                    self.logger.info(f"Applying migration {filename}...")
                    filepath = os.path.join(migrations_dir, filename)
                    with open(filepath, "r") as f:
                        sql_script = f.read()

                    print(f"Executing migration script: {filename}")
                    print(sql_script)

                    try:
                        with conn:  # Execute in a transaction
                            conn.executescript(sql_script)
                            conn.execute(
                                queries.INSERT_SCHEMA_VERSION,
                                (version, datetime.now().isoformat()),
                            )
                        self.logger.info(f"Migration {filename} applied successfully.")
                        current_version = version
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" in str(e):
                            self.logger.warning(
                                f"Migration {filename} failed because a column already exists. Assuming it was already applied and continuing."
                            )
                            conn.execute(
                                queries.INSERT_SCHEMA_VERSION,
                                (version, datetime.now().isoformat()),
                            )
                            current_version = version
                        else:
                            raise e
                else:
                    self.logger.debug(f"Migration {filename} already applied.")
            self.logger.info("Database migration check complete.")
        except Exception as e:
            self.logger.error(f"Error during database migration: {e}", exc_info=True)
            raise
        finally:
            self._close_conn()  # Ensure connection is closed after migrations

    def _deserialize_rows(self, rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
        """Deserializes JSON strings from database rows into a clean dictionary, prioritizing top-level columns."""
        results = []

        json_keys = [
            "blueprint_data", "ai_content_json", "in_article_images_data",
            "social_media_posts_json", "final_package_json", "wordpress_payload_json",
            "score_breakdown", "full_data", "search_volume_trend_json",
            "competitor_social_media_tags_json", "competitor_page_timing_json",
            "keyword_info", "keyword_properties", "search_intent_info", "serp_overview",
            "metrics_history", "related_keywords", "keyword_categories",
            "discovery_goal" # NEW: Add this new key
        ]

        for row in rows:
            final_item = dict(row)

            for key in json_keys:
                if key in final_item and isinstance(final_item[key], str):
                    try:
                        final_item[key] = json.loads(final_item[key])
                    except json.JSONDecodeError:
                        final_item[key] = None
            
            self.logger.info(f"Before backfill: {final_item}")
            self.logger.info(f"Before backfill: {final_item}")
            # Backward compatibility: If top-level fields are null, pull from full_data
            full_data = final_item.get('full_data') or {}
            if isinstance(full_data, str):
                try:
                    full_data = json.loads(full_data)
                except json.JSONDecodeError:
                    full_data = {}

            if final_item.get('search_volume') is None:
                final_item['search_volume'] = (full_data.get('keyword_info') or {}).get('search_volume')
            
            if final_item.get('keyword_difficulty') is None:
                final_item['keyword_difficulty'] = (full_data.get('keyword_properties') or {}).get('keyword_difficulty')
            self.logger.info(f"After backfill: {final_item}")
            self.logger.info(f"After backfill: {final_item}")

            # Reconstruct nested objects for any part of the app that might still use them
            final_item['keyword_info'] = final_item.get('keyword_info') or {}
            final_item['keyword_properties'] = final_item.get('keyword_properties') or {}
            final_item['search_intent_info'] = final_item.get('search_intent_info') or {}
            
            final_item['keyword_info']['search_volume'] = final_item.get('search_volume')
            final_item['keyword_info']['cpc'] = final_item.get('cpc')
            final_item['keyword_info']['competition'] = final_item.get('competition')
            
            final_item['keyword_properties']['keyword_difficulty'] = final_item.get('keyword_difficulty')
            final_item['search_intent_info']['main_intent'] = final_item.get('main_intent')

            if "blueprint_data" in final_item:
                final_item["blueprint"] = final_item.pop("blueprint_data")
            if "ai_content_json" in final_item:
                final_item["ai_content"] = final_item.pop("ai_content_json")

            results.append(final_item)
        return results

    def add_opportunity(self, client_id: str, opportunity_data: Dict[str, Any]):
        """Adds a new opportunity to the database from a dictionary."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO opportunities (
                    keyword, client_id, status, date_added, date_processed, 
                    strategic_score, keyword_info, keyword_properties, 
                    search_intent_info, serp_overview, score_breakdown, ai_content_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    opportunity_data.get("keyword"),
                    client_id,
                    opportunity_data.get("status", "pending"),
                    opportunity_data.get("date_added", datetime.now().isoformat()),
                    opportunity_data.get("date_processed"),
                    opportunity_data.get("strategic_score"),
                    json.dumps(opportunity_data.get("keyword_info")),
                    json.dumps(opportunity_data.get("keyword_properties")),
                    json.dumps(opportunity_data.get("search_intent_info")),
                    json.dumps(opportunity_data.get("serp_overview")),
                    json.dumps(opportunity_data.get("score_breakdown")),
                    json.dumps(opportunity_data.get("ai_content")),
                ),
            )
            return cursor.lastrowid

    def add_opportunities(
        self, opportunities: List[Dict[str, Any]], client_id: str, run_id: int, discovery_goal: Optional[str] = None
    ) -> int:
        """Adds multiple opportunities to the database in a single transaction, updating existing ones."""
        conn = self._get_conn()
        num_added = 0
        with conn:
            cursor = conn.cursor()
            for opp in opportunities:
                keyword = opp.get("keyword")
                cursor.execute("SELECT id FROM keywords WHERE keyword = ?", (keyword,))
                keyword_row = cursor.fetchone()

                keyword_info = opp.get("keyword_info", {})
                keyword_properties = opp.get("keyword_properties", {})
                search_intent_info = opp.get("search_intent_info", {})

                if keyword_row:
                    keyword_id = keyword_row["id"]
                    # Update existing keyword
                    cursor.execute(
                        """
                        UPDATE keywords
                        SET search_volume = ?, keyword_difficulty = ?, cpc = ?, competition = ?, search_volume_trend = ?, main_intent = ?, core_keyword = ?
                        WHERE id = ?
                    """,
                        (
                            keyword_info.get("search_volume"),
                            keyword_properties.get("keyword_difficulty"),
                            keyword_info.get("cpc"),
                            keyword_info.get("competition"),
                            json.dumps(keyword_info.get("search_volume_trend")),
                            search_intent_info.get("main_intent"),
                            keyword_properties.get("core_keyword"),
                            keyword_id,
                        ),
                    )
                else:
                    # Insert new keyword
                    cursor.execute(
                        """
                        INSERT INTO keywords (keyword, search_volume, keyword_difficulty, cpc, competition, search_volume_trend, main_intent, core_keyword)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            keyword,
                            keyword_info.get("search_volume"),
                            keyword_properties.get("keyword_difficulty"),
                            keyword_info.get("cpc"),
                            keyword_info.get("competition"),
                            json.dumps(keyword_info.get("search_volume_trend")),
                            search_intent_info.get("main_intent"),
                            keyword_properties.get("core_keyword"),
                        ),
                    )
                    keyword_id = cursor.lastrowid

                cursor.execute(
                    "SELECT id, metrics_history FROM opportunities WHERE client_id = ? AND keyword_id = ?",
                    (client_id, keyword_id),
                )
                opportunity_row = cursor.fetchone()

                if opportunity_row:
                    # Update existing opportunity
                    history = (
                        json.loads(opportunity_row["metrics_history"])
                        if opportunity_row["metrics_history"]
                        else []
                    )
                    history.append(
                        {
                            "date": datetime.now().isoformat(),
                            "search_volume": keyword_info.get("search_volume"),
                            "keyword_difficulty": keyword_properties.get(
                                "keyword_difficulty"
                            ),
                            "cpc": keyword_info.get("cpc"),
                        }
                    )
                    cursor.execute(
                        """
                        UPDATE opportunities
                        SET last_seen_at = ?, metrics_history = ?, search_volume = ?, keyword_difficulty = ?
                        WHERE id = ?
                    """,
                        (
                            datetime.now().isoformat(),
                            json.dumps(history),
                            keyword_info.get("search_volume"),
                            keyword_properties.get("keyword_difficulty"),
                            opportunity_row["id"],
                        ),
                    )
                else:
                    # Insert new opportunity
                    num_added += 1
                    # Extract values for direct columns, potentially nulling them out from JSON if no longer needed there
                    cpc_val = keyword_info.get("cpc")
                    competition_val = keyword_info.get("competition")
                    main_intent_val = search_intent_info.get("main_intent")
                    search_volume_trend_json_val = json.dumps(
                        keyword_info.get("search_volume_trend")
                    )

                    # Aggregate top competitor data for direct columns
                    top_competitor = next(
                        (
                            comp
                            for comp in opp.get("blueprint", {}).get(
                                "competitor_analysis", []
                            )
                            if comp.get("url")
                        ),
                        None,
                    )
                    competitor_social_media_tags_json_val = (
                        json.dumps(top_competitor.get("social_media_tags", {}))
                        if top_competitor
                        else None
                    )
                    competitor_page_timing_json_val = (
                        json.dumps(top_competitor.get("page_timing", {}))
                        if top_competitor
                        else None
                    )

                    # Create a copy of the opportunity data to avoid modifying the original object in memory
                    full_data_copy = opp.copy()
                    # Remove keys that are now stored in dedicated top-level columns to prevent data duplication.
                    # This only applies to new records being inserted.
                    full_data_copy.pop("keyword_info", None)
                    full_data_copy.pop("keyword_properties", None)
                    full_data_copy.pop("search_intent_info", None)
                    
                    # Check if 'discovery_goal' column exists in the opportunities table
                    cursor.execute("PRAGMA table_info(opportunities)")
                    opportunities_columns = [col[1] for col in cursor.fetchall()]

                    insert_columns = [
                        "keyword", "client_id", "run_id", "status", "date_added", "date_processed",
                        "strategic_score", "blog_qualification_status", "blog_qualification_reason",
                        "keyword_info", "keyword_properties",
                        "search_intent_info", "serp_overview", "score_breakdown", "ai_content_json",
                        "keyword_info_normalized_with_bing", "keyword_info_normalized_with_clickstream", "monthly_searches", "traffic_value",
                        "check_url", "related_keywords", "keyword_categories", "core_keyword", "last_seen_at", "metrics_history", "keyword_id",
                        "full_data",
                        "cpc", "competition", "main_intent", "search_volume_trend_json",
                        "competitor_social_media_tags_json", "competitor_page_timing_json",
                        "social_media_posts_status", "search_volume", "keyword_difficulty",
                    ]
                    insert_values = [
                        keyword,
                        client_id,
                        run_id,
                        opp.get("status", "pending"),
                        opp.get("date_added", datetime.now().isoformat()),
                        opp.get("date_processed"),
                        opp.get("strategic_score"),
                        opp.get("blog_qualification_status"),
                        opp.get("blog_qualification_reason"),
                        json.dumps(keyword_info),
                        json.dumps(keyword_properties),
                        json.dumps(search_intent_info),
                        json.dumps(opp.get("serp_overview")),
                        json.dumps(opp.get("score_breakdown")),
                        json.dumps(opp.get("ai_content")),
                        json.dumps(opp.get("keyword_info_normalized_with_bing")),
                        json.dumps(
                            opp.get("keyword_info_normalized_with_clickstream")
                        ),
                        json.dumps(keyword_info.get("monthly_searches")),
                        opp.get("traffic_value", 0),
                        opp.get("serp_info", {}).get("check_url"),
                        json.dumps(opp.get("related_keywords")),
                        json.dumps(keyword_info.get("categories")),
                        keyword_properties.get("core_keyword"),
                        datetime.now().isoformat(),
                        json.dumps([]),
                        keyword_id,
                        json.dumps(full_data_copy),
                        cpc_val,
                        competition_val,
                        main_intent_val,
                        search_volume_trend_json_val,
                        competitor_social_media_tags_json_val,
                        competitor_page_timing_json_val,
                        opp.get("social_media_posts_status", "draft"),
                        keyword_info.get("search_volume"),
                        keyword_properties.get("keyword_difficulty"),
                    ]

                    if "discovery_goal" in opportunities_columns:
                        insert_columns.append("discovery_goal")
                        insert_values.append(discovery_goal)

                    placeholders = ", ".join(["?"] * len(insert_columns))
                    columns_str = ", ".join(insert_columns)

                    cursor.execute(
                        f"""
                        INSERT INTO opportunities ({columns_str})
                        VALUES ({placeholders})
                        """,
                        tuple(insert_values),
                    )

        return num_added

    def get_opportunity_queue(self, client_id: str = "default") -> List[Dict[str, Any]]:
        """Retrieves all pending opportunities for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_PENDING_OPPORTUNITIES, (client_id,))
            return self._deserialize_rows(cursor.fetchall())

    def get_all_opportunities(
        self,
        client_id: str,
        params: Dict[str, Any],
        summary: bool = False,
        select_columns: str = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Retrieves keyword opportunities for a client, supporting filtering, sorting, and pagination.
        If summary is True, only essential fields for the table view are returned.
        """
        conn = self._get_conn()
        limit = int(params.get("limit", 20))
        page = int(params.get("page", 1))
        offset = (page - 1) * limit

        sort_by_map = {
            "strategic_score": "strategic_score",
            "date_added": "date_added",
            "keyword": "keyword",
            "status": "status",
            "search_volume": "JSON_EXTRACT(full_data, '$.keyword_info.search_volume')",
            "keyword_difficulty": "JSON_EXTRACT(full_data, '$.keyword_properties.keyword_difficulty')",
            "cpc": "JSON_EXTRACT(full_data, '$.keyword_info.cpc')",
        }
        sort_by = sort_by_map.get(params.get("sort_by"), "date_added")
        sort_direction = "ASC" if params.get("sort_direction") == "asc" else "DESC"

        where_parts = ["client_id = ?"]
        query_values = [client_id]

        status_filter = params.get("status")
        if status_filter:
            statuses = [s.strip() for s in status_filter.split(",")]
            placeholders = ",".join(["?"] * len(statuses))
            where_parts.append(f"status IN ({placeholders})")
            query_values.extend(statuses)

        where_clause = " AND ".join(where_parts)

        count_query = f"SELECT COUNT(*) FROM opportunities WHERE {where_clause}"
        with conn:
            cursor = conn.cursor()
            cursor.execute(count_query, query_values)
            total_count = cursor.fetchone()[0]

        select_columns = (
            select_columns
            if select_columns
            else "id, keyword, status, date_added, strategic_score, search_volume, keyword_difficulty, cpc, competition, main_intent, search_volume_trend_json, competitor_social_media_tags_json, competitor_page_timing_json, blog_qualification_status, latest_job_id, cluster_name, score_breakdown, full_data"
        )
        if summary and "full_data" not in select_columns:
            select_columns += ", full_data"

        final_query = f"SELECT {select_columns} FROM opportunities WHERE {where_clause} ORDER BY {sort_by} {sort_direction} LIMIT ? OFFSET ?"

        paged_values = query_values + [limit, offset]
        with conn:
            cursor = conn.cursor()
            cursor.execute(final_query, paged_values)
            opportunities = self._deserialize_rows(cursor.fetchall())

        return opportunities, total_count

    def get_opportunity_by_id(self, opportunity_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single opportunity by its primary key ID."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_OPPORTUNITY_BY_ID, (opportunity_id,))
            row = cursor.fetchone()
            if row:
                return self._deserialize_rows([row])[0]
        return None

    def get_opportunity_summary_by_id(
        self, opportunity_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves only essential summary fields for an opportunity. (W13 FIX)
        """
        conn = self._get_conn()
        with conn:
            # Use a selective query to avoid fetching large JSON blobs
            cursor = conn.execute(
                "SELECT id, keyword, status, date_added, strategic_score, blog_qualification_status, featured_image_local_path FROM opportunities WHERE id = ?",
                (opportunity_id,),
            )
            row = cursor.fetchone()
            if row:
                # Need to manually or selectively deserialize, but for simplicity, we treat the row as the summary
                return dict(row)
            return None

    def get_opportunity_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single opportunity by its URL slug."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_OPPORTUNITY_BY_SLUG, (slug,))
            row = cursor.fetchone()
            if row:
                return self._deserialize_rows([row])[0]
        return None

    def search_opportunities(self, client_id: str, query: str) -> List[Dict[str, Any]]:
        """Searches for opportunities by keyword for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute(
                queries.SEARCH_OPPORTUNITIES_BY_KEYWORD, (client_id, search_term)
            )
            # No need for full deserialization as we are fetching simple columns
            return [dict(row) for row in cursor.fetchall()]

    def get_published_articles_for_linking(
        self, client_id: str
    ) -> List[Dict[str, str]]:
        """
        Retrieves a list of published articles (title and slug) for internal linking suggestions.
        """
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            # Select only 'keyword' (as title) and 'slug' for published articles
            # 'full_data' is not needed here to save memory/processing
            cursor.execute(
                """
                SELECT keyword, slug FROM opportunities
                WHERE client_id = ? AND status IN ('generated', 'published') AND slug IS NOT NULL;
            """,
                (client_id,),
            )

            articles = []
            for row in cursor.fetchall():
                articles.append(
                    {
                        "title": row["keyword"],  # Use keyword as a proxy for title
                        "url": f"/article/{row['slug']}",  # Construct the relative URL
                    }
                )
            return articles

    def get_all_processed_keywords_for_client(self, client_id: str) -> List[str]:
        """Retrieves a flat list of all primary keywords for a client that are not in a 'rejected' or 'failed' state."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_ALL_PROCESSED_KEYWORDS, (client_id,))
            return [row["keyword"] for row in cursor.fetchall()]

    def check_existing_keywords(self, client_id: str, keywords: List[str]) -> List[str]:
        """Checks a list of keywords against the DB and returns those that exist."""
        if not keywords:
            return []
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            placeholders = ",".join("?" for _ in keywords)
            query = f"SELECT keyword FROM opportunities WHERE client_id = ? AND keyword IN ({placeholders})"
            cursor.execute(query, [client_id] + keywords)
            return [row["keyword"] for row in cursor.fetchall()]

    def update_opportunity_status(self, opportunity_id: int, new_status: str):
        """Updates a keyword's status in the database."""
        conn = self._get_conn()
        with conn:
            if new_status in ["generated", "analyzed", "failed"]:
                conn.execute(
                    queries.UPDATE_OPPORTUNITY_STATUS_WITH_DATE,
                    (new_status, datetime.now().isoformat(), opportunity_id),
                )
            else:
                conn.execute(
                    queries.UPDATE_OPPORTUNITY_STATUS, (new_status, opportunity_id)
                )

    def update_opportunity_workflow_state(
        self,
        opportunity_id: int,
        step: str,
        status: str = "in_progress",
        error_message: Optional[str] = None,
    ):
        """Updates the workflow step and status for a given opportunity.
        Possible statuses include: 'in_progress', 'completed', 'failed', 'pending', 'validated', 'analyzed', 'generated', 'published', 'rejected', 'paused_for_approval'."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Updating workflow state to step='{step}', status='{status}'"
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_WORKFLOW_STATE,
                (step, status, error_message, opportunity_id),
            )

    def update_opportunity_blueprint(
        self, opportunity_id: int, blueprint_data: Dict[str, Any], slug: str
    ):
        """Stores the generated blueprint data and the URL slug for a specific opportunity."""
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_BLUEPRINT_AND_SLUG,
                (json.dumps(blueprint_data), slug, opportunity_id),
            )

    def update_opportunity_ai_content(
        self, opportunity_id: int, ai_content_data: Dict[str, Any], ai_model: str
    ):
        """
        Stores the generated AI content package and model used for a specific opportunity.
        Applies server-side sanitization to the HTML body (W20 FIX).
        """
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving AI content generated by model '{ai_model}'."
        )

        # W20 FIX: Sanitize content before saving
        html_body = ai_content_data.get("article_body_html")
        if html_body:
            clean_html = bleach.clean(
                html_body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES_DB
            )
            ai_content_data["article_body_html"] = clean_html

        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_AI_CONTENT,
                (
                    json.dumps(ai_content_data),
                    ai_model,
                    datetime.now().isoformat(),
                    opportunity_id,
                ),
            )

    def update_opportunity_images(
        self,
        opportunity_id: int,
        featured_image_url: Optional[str],
        featured_image_local_path: Optional[str],
        in_article_images_data: List[Dict[str, Any]],
    ):
        """Stores image generation details for a specific opportunity."""
        # W5 FIX: Ensure path is relative before storing, e.g., by checking if it starts with the expected API prefix
        if featured_image_local_path and os.path.isabs(featured_image_local_path):
            # Assuming the standard path is relative to the API's image mounting point,
            # extract the filename or the relative part required by the API
            # This is a simplified example; robust path management is needed.
            base_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "generated_images")
            )
            featured_image_local_path = os.path.relpath(
                featured_image_local_path, base_path
            )

        self.logger.info(
            f"Opportunity {opportunity_id}: Saving Pexels image data (featured URL: {featured_image_url})."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_IMAGES,
                (
                    featured_image_url,
                    featured_image_local_path,
                    json.dumps(in_article_images_data),
                    opportunity_id,
                ),
            )

    def update_opportunity_full_data(
        self, opportunity_id: int, full_data: Dict[str, Any]
    ):
        """Updates the full_data JSON blob for a specific opportunity."""
        self.logger.info(f"Opportunity {opportunity_id}: Updating full_data field.")
        conn = self._get_conn()
        with conn:
            conn.execute(
                "UPDATE opportunities SET full_data = ? WHERE id = ?",
                (json.dumps(full_data), opportunity_id),
            )

    def update_opportunity_scores(
        self,
        opportunity_id: int,
        strategic_score: float,
        score_breakdown: Dict[str, Any],
        blueprint_data: Optional[Dict[str, Any]] = None,
    ):
        """Updates the primary strategic score, breakdown, and blueprint for an opportunity."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Updating strategic_score to {strategic_score:.2f} and saving blueprint."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_SCORES,
                (
                    strategic_score,
                    json.dumps(score_breakdown),
                    json.dumps(blueprint_data) if blueprint_data else None,
                    opportunity_id,
                ),
            )

    def update_opportunity_final_package(
        self, opportunity_id: int, final_package: Dict[str, Any]
    ):
        """Stores the generated final content package JSON for a specific opportunity."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving final standalone content package."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_FINAL_PACKAGE,
                (json.dumps(final_package), opportunity_id),
            )

    def add_client(
        self, client_id: str, client_name: str, default_settings: Dict[str, Any]
    ) -> bool:
        """Adds a new client to the clients table and initializes their settings."""
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.execute("PRAGMA table_info(client_settings)")
                schema_columns = {row["name"] for row in cursor.fetchall()}

                conn.execute(
                    queries.INSERT_CLIENT,
                    (client_id, client_name, datetime.now().isoformat()),
                )

                settings_to_insert = {
                    k: v for k, v in default_settings.items() if k in schema_columns
                }
                if (
                    "client_knowledge_base" not in settings_to_insert
                    and "client_knowledge_base" in schema_columns
                ):
                    settings_to_insert["client_knowledge_base"] = (
                        ""  # Initialize with empty string
                    )
                settings_to_insert["client_id"] = client_id
                settings_to_insert["last_updated"] = datetime.now().isoformat()

                keys = ", ".join(settings_to_insert.keys())
                placeholders = ", ".join("?" * len(settings_to_insert))

                values = []
                for key in settings_to_insert.keys():
                    value = settings_to_insert[key]
                    if isinstance(value, list):
                        values.append(",".join(map(str, value)))
                    elif isinstance(value, bool):
                        values.append(1 if value else 0)
                    else:
                        values.append(value)

                insert_query = (
                    f"INSERT INTO client_settings ({keys}) VALUES ({placeholders})"
                )

                conn.execute(insert_query, tuple(values))
                self.logger.info(
                    f"Added new client '{client_name}' ({client_id}) and initialized settings."
                )

                # Also initialize qualification settings with a comprehensive set of default values
                conn.execute(
                    """
                    INSERT INTO qualification_settings (
                        client_id, ease_of_ranking_weight, traffic_potential_weight, commercial_intent_weight,
                        serp_features_weight, growth_trend_weight, serp_freshness_weight, serp_volatility_weight,
                        competitor_weakness_weight, competitor_performance_weight, min_search_volume, max_keyword_difficulty,
                        negative_keywords, prohibited_intents, max_y_pixel_threshold,
                        max_forum_results_in_top_10, max_ecommerce_results_in_top_10,
                        disallowed_page_types_in_top_3
                    ) VALUES (?, 40, 15, 5, 5, 5, 5, 5, 20, 5, 100, 80, 'login,free,cheap', 'navigational', 800, 3, 2, 'E-commerce,Forum')
                """,
                    (client_id,),
                )
                self.logger.info(
                    f"Initialized default qualification settings for client '{client_name}' ({client_id})."
                )
            return True
        except sqlite3.IntegrityError:
            self.logger.warning(f"Client with ID '{client_id}' already exists.")
            return False
        except Exception as e:
            self.logger.error(
                f"Error adding client '{client_name}': {e}", exc_info=True
            )
            return False

    def get_clients(self) -> List[Dict[str, str]]:
        """Retrieves all clients from the database."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_ALL_CLIENTS)
            return [dict(row) for row in cursor.fetchall()]

    def get_processed_opportunities(self, client_id: str) -> List[Dict[str, Any]]:
        """Retrieves all opportunities with a generated blueprint for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_PROCESSED_OPPORTUNITIES, (client_id,))
            return self._deserialize_rows(cursor.fetchall())

    def get_client_settings(self, client_id: str) -> Dict[str, Any]:
        """Retrieves settings for a specific client, converting from DB types."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_CLIENT_SETTINGS, (client_id,))
            row = cursor.fetchone()
            if row:
                settings = dict(row)
                settings.pop("client_id", None)
                settings.pop("last_updated", None)

                list_keys = [
                    "allowed_intents",
                    "negative_keywords",
                    "competitor_blacklist_domains",
                    "serp_feature_filters",
                    "serp_features_exclude_filter",
                    "platforms",
                    "default_wordpress_categories",
                    "default_wordpress_tags",
                    "ugc_and_parasite_domains",
                    "high_value_categories",
                    "hostile_serp_features",
                    "final_validation_non_blog_domains",
                    "prohibited_intents",
                    "discovery_goals", # NEW: Handle discovery_goals as a list
                ]
                for key in list_keys:
                    if settings.get(key) is not None and isinstance(settings[key], str):
                        settings[key] = [
                            item.strip()
                            for item in settings[key].split(",")
                            if item.strip()
                        ]
                    elif settings.get(key) is None:
                        settings[key] = []

                bool_keys = [
                    "enforce_intent_filter",
                    "require_question_keywords",
                    "use_pexels_first",
                    "cleanup_local_images",
                    "onpage_enable_javascript",
                    "onpage_load_resources",
                    "calculate_rectangles",
                    "onpage_disable_cookie_popup",
                    "onpage_return_despite_timeout",
                    "onpage_enable_browser_rendering",
                    "onpage_store_raw_html",
                    "onpage_validate_micromarkup",
                    "discovery_replace_with_core_keyword",
                    "discovery_ignore_synonyms",
                    "enable_automated_internal_linking",  # NEW
                ]
                for key in bool_keys:
                    if settings.get(key) is not None:
                        settings[key] = bool(settings[key])

                int_keys = [
                    "num_in_article_images",
                    "location_code",
                    "serp_freshness_old_threshold_days",
                    "min_competitor_word_count",
                    "max_competitor_technical_warnings",
                    "num_competitors_to_analyze",
                    "num_common_headings",
                    "num_unique_angles",
                    "max_initial_serp_urls_to_analyze",
                    "min_search_volume",
                    "max_keyword_difficulty",
                    "people_also_ask_click_depth",
                    "onpage_max_domains_per_request",
                    "onpage_max_tasks_per_request",
                    "ease_of_ranking_weight",
                    "traffic_potential_weight",
                    "commercial_intent_weight",
                    "growth_trend_weight",
                    "serp_features_weight",
                    "serp_freshness_weight",
                    "serp_volatility_weight",
                    "competitor_weakness_weight",
                    "max_sv_for_scoring",
                    "max_domain_rank_for_scoring",
                    "max_referring_domains_for_scoring",
                    "serp_volatility_stable_threshold_days",
                    "discovery_related_depth",
                    "max_avg_referring_domains_filter",
                    "yearly_trend_decline_threshold",
                    "quarterly_trend_decline_threshold",
                    "max_kd_hard_limit",
                    "max_referring_main_domains_limit",
                    "max_avg_domain_rank_threshold",
                    "min_keyword_word_count",
                    "max_keyword_word_count",
                    "crowded_serp_features_threshold",
                    "min_serp_stability_days",
                    "max_non_blog_results",
                    "max_ai_overview_words",
                    "max_first_organic_y_pixel",
                    "max_words_for_ai_analysis",  # NEW
                    "max_avg_lcp_time",  # NEW
                ]
                for key in int_keys:
                    if settings.get(key) is not None:
                        try:
                            settings[key] = int(settings[key])
                        except (ValueError, TypeError):
                            pass

                float_keys = [
                    "informational_score",
                    "commercial_score",
                    "transactional_score",
                    "navigational_score",
                    "question_keyword_bonus",
                    "max_cpc_for_scoring",
                    "min_monthly_trend_percentage",
                    "featured_snippet_bonus",
                    "ai_overview_bonus",
                    "serp_freshness_bonus_max",
                    "min_cpc_filter_api",
                    "category_intent_bonus",
                    "search_volume_volatility_threshold",
                    "max_paid_competition_score",
                    "max_high_top_of_page_bid",
                    "max_pages_to_domain_ratio",
                    "ai_generation_temperature",  # NEW
                    "recommended_word_count_multiplier",  # NEW
                ]
                for key in float_keys:
                    if settings.get(key) is not None:
                        try:
                            settings[key] = float(settings[key])
                        except (ValueError, TypeError):
                            pass

                return settings
            return {}

    def update_client_settings(self, client_id: str, settings: Dict[str, Any]):
        """Updates client-specific settings, handling type conversions for DB storage."""
        self.logger.info(f"Updating client settings for {client_id}.")
        conn = self._get_conn()
        with conn:
            cursor = conn.execute("PRAGMA table_info(client_settings)")
            schema_columns = {row["name"] for row in cursor.fetchall()}

            current_time = datetime.now().isoformat()

            set_clauses = ["last_updated = ?"]
            values = [current_time]

            for key, value in settings.items():
                if key in schema_columns and key not in ["client_id", "last_updated"]:
                    if isinstance(value, list):
                        # Convert lists to comma-separated strings for DB storage
                        db_value = ",".join(map(str, value))
                    elif isinstance(value, bool):
                        db_value = 1 if value else 0
                    elif key in ['brand_tone', 'target_audience', 'terms_to_avoid', 'expert_persona']:
                        # For sensitive text fields, strip all HTML.
                        db_value = bleach.clean(str(value), tags=[], strip=True)
                    elif key == 'client_knowledge_base':
                        # For client_knowledge_base, allow a specific set of safe HTML tags for richer content.
                        KB_ALLOWED_TAGS = ['p', 'br', 'b', 'strong', 'i', 'em', 'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3']
                        KB_ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}
                        db_value = bleach.clean(str(value), tags=KB_ALLOWED_TAGS, attributes=KB_ALLOWED_ATTRIBUTES, strip=True)
                    elif key == 'onpage_custom_checks_thresholds':
                        # If it's meant to be a JSON string, ensure it's stored as one.
                        if isinstance(value, dict):
                            db_value = json.dumps(value)
                        else:
                            db_value = str(value)
                    # For other string types (like custom_prompt_template), store directly
                    else:
                        db_value = value

                    set_clauses.append(f"{key} = ?")
                    values.append(db_value)

            if len(set_clauses) > 1:
                update_query = f"UPDATE client_settings SET {', '.join(set_clauses)} WHERE client_id = ?"
                values.append(client_id)
                conn.execute(update_query, values)
                self.logger.info(f"Client settings for {client_id} updated in DB.")
            else:
                self.logger.info(
                    f"No valid client settings found to update for {client_id}."
                )

    def get_all_opportunities_for_export(self) -> List[Dict[str, Any]]:
        """Retrieves all opportunities for all clients from the database."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_ALL_OPPORTUNITIES_FOR_EXPORT)
            return self._deserialize_rows(cursor.fetchall())

    def get_dashboard_stats(self, client_id: str) -> Dict[str, Any]:
        """Retrieves statistics for the dashboard UI."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()

            # Get counts by status
            cursor.execute(queries.COUNT_OPPORTUNITIES_BY_STATUS, (client_id,))
            status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

            # Get recent items
            cursor.execute(queries.SELECT_RECENTLY_GENERATED, (client_id,))
            recent_items = [dict(row) for row in cursor.fetchall()]

            return {"status_counts": status_counts, "recent_items": recent_items}

    def get_total_api_cost(self, client_id: str) -> float:
        """Calculates the total API cost for a client by summing costs from both opportunities and discovery runs."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            
            # Sum cost from opportunities
            cursor.execute(
                "SELECT SUM(total_api_cost) FROM opportunities WHERE client_id = ?",
                (client_id,),
            )
            opportunities_cost = cursor.fetchone()[0] or 0.0
            
            # Sum cost from discovery runs
            cursor.execute(
                "SELECT SUM(total_api_cost) FROM discovery_runs WHERE client_id = ?",
                (client_id,),
            )
            runs_cost = cursor.fetchone()[0] or 0.0
            
            return opportunities_cost + runs_cost

    def get_dashboard_data(self, client_id: str) -> Dict[str, Any]:
        """Retrieves aggregated data for the main dashboard UI."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()

            # 1. KPIs
            cursor.execute(
                "SELECT COUNT(*) FROM opportunities WHERE client_id = ?", (client_id,)
            )
            total_opportunities = cursor.fetchone()[0]
            cursor.execute(
                "SELECT COUNT(*) FROM opportunities WHERE client_id = ? AND status = 'generated'",
                (client_id,),
            )
            content_generated = cursor.fetchone()[0]
            cursor.execute(
                "SELECT SUM(traffic_value) FROM opportunities WHERE client_id = ?",
                (client_id,),
            )
            total_traffic_value = cursor.fetchone()[0] or 0
            total_api_cost = self.get_total_api_cost(client_id)

            kpis = {
                "totalOpportunities": total_opportunities,
                "contentGenerated": content_generated,
                "totalTrafficValue": total_traffic_value,
                "totalApiCost": total_api_cost,
            }

            # 2. Funnel and Stats Data
            dashboard_stats = self.get_dashboard_stats(client_id)
            status_counts = dashboard_stats.get("status_counts", {})
            recent_items = dashboard_stats.get("recent_items", [])

            funnel_data = [
                {"stage": "Total", "count": total_opportunities},
                {"stage": "Validated", "count": status_counts.get("validated", 0)},
                {"stage": "Analyzed", "count": status_counts.get("analyzed", 0)},
                {"stage": "Generated", "count": content_generated},
                {"stage": "Disqualified", "count": (status_counts.get("rejected", 0) or 0) + (status_counts.get("failed", 0) or 0)},
            ]

            # 3. Action Items
            cursor.execute(queries.SELECT_ACTION_ITEMS, (client_id,))
            action_items_raw = [dict(row) for row in cursor.fetchall()]
            action_items = {
                "awaitingApproval": [
                    item
                    for item in action_items_raw
                    if item["status"] == "paused_for_approval"
                ],
                "failed": [
                    item for item in action_items_raw if item["status"] == "failed"
                ],
            }

            return {
                "kpis": kpis,
                "funnelData": funnel_data,
                "actionItems": action_items,
                "status_counts": status_counts,
                "recent_items": recent_items,
            }

    def update_opportunity_wordpress_payload(
        self, opportunity_id: int, wordpress_payload: Dict[str, Any]
    ):
        """Stores the generated WordPress JSON payload for a specific opportunity."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving final WordPress JSON payload."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_WORDPRESS_PAYLOAD,
                (json.dumps(wordpress_payload), opportunity_id),
            )

    def get_api_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves a cached item from the api_cache table."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(queries.SELECT_API_CACHE, (key,))
            row = cursor.fetchone()
            if row:
                # Check TTL during retrieval
                if row["timestamp"] + (row["ttl_days"] * 86400) > time.time():
                    return json.loads(row["data"])
                else:
                    self.logger.debug(f"Cache STALE for key: {key}")
                    self.delete_api_cache_by_key(key)  # Clean up stale entry
            return None

    def set_api_cache(self, key: str, value: Any, ttl_days: int = 7):
        """Stores an item in the api_cache table."""
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.INSERT_API_CACHE,
                (key, json.dumps(value), time.time(), ttl_days),
            )
        self.logger.debug(f"Cache SET for key: {key}")

    def delete_api_cache_by_key(self, key: str):
        """Deletes a specific item from the api_cache table."""
        conn = self._get_conn()
        with conn:
            conn.execute(queries.DELETE_API_CACHE_BY_KEY, (key,))

    def clear_api_cache(self):
        """Clears all items from the api_cache table."""
        conn = self._get_conn()
        with conn:
            conn.execute(queries.TRUNCATE_API_CACHE)
        self.logger.info("API cache cleared.")

    def clear_expired_api_cache(self):
        """Deletes all expired items from the api_cache table."""
        conn = self._get_conn()
        with conn:
            conn.execute(queries.DELETE_EXPIRED_API_CACHE, (time.time(),))
        self.logger.debug("Expired API cache entries cleaned up.")

    # --- Discovery Run Methods ---

    def create_discovery_run(self, client_id: str, parameters: Dict[str, Any]) -> int:
        """Creates a new discovery run record and returns its ID."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                queries.INSERT_DISCOVERY_RUN,
                (
                    client_id,
                    datetime.now().isoformat(),
                    "running",
                    json.dumps(parameters),
                ),
            )
            return cursor.lastrowid

    def update_discovery_run_status(self, run_id: int, status: str):
        """Updates the status of a discovery run."""
        conn = self._get_conn()
        with conn:
            conn.execute(queries.UPDATE_DISCOVERY_RUN_STATUS, (status, run_id))

    def update_discovery_run_completed(
        self, run_id: int, results_summary: Dict[str, Any]
    ):
        """Marks a discovery run as completed and stores the results summary."""
        conn = self._get_conn()
        total_cost = results_summary.get("total_cost", 0.0)
        with conn:
            conn.execute(
                queries.UPDATE_DISCOVERY_RUN_COMPLETED,
                (
                    datetime.now().isoformat(),
                    json.dumps(results_summary),
                    total_cost,
                    run_id,
                ),
            )

    def update_discovery_run_failed(self, run_id: int, error_message: str):
        """Marks a discovery run as failed and stores the error message."""
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_DISCOVERY_RUN_FAILED,
                (datetime.now().isoformat(), error_message, run_id),
            )

    def get_all_discovery_runs_paginated(
        self, client_id: str, page: int, limit: int, filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Retrieves all discovery runs for a specific client with pagination and filtering."""
        conn = self._get_conn()
        
        base_query = "FROM discovery_runs WHERE client_id = ?"
        query_params = [client_id]
        
        where_clauses = []
        if filters:
            if filters.get("search_query"):
                where_clauses.append("(parameters LIKE ? OR status LIKE ?)")
                search_term = f"%{filters['search_query']}%"
                query_params.extend([search_term, search_term])
            if filters.get("start_date") and filters.get("end_date"):
                where_clauses.append("start_time BETWEEN ? AND ?")
                query_params.extend([filters["start_date"], filters["end_date"]])

        if where_clauses:
            base_query += " AND " + " AND ".join(where_clauses)

        with conn:
            cursor = conn.cursor()
            
            # Get total count with filters
            count_query = f"SELECT COUNT(*) {base_query}"
            cursor.execute(count_query, query_params)
            total_count = cursor.fetchone()[0]
            
            # Get paginated data with filters
            select_query = f"SELECT * {base_query} ORDER BY start_time DESC LIMIT ? OFFSET ?"
            cursor.execute(select_query, query_params + [limit, (page - 1) * limit])
            
            runs = []
            for row in cursor.fetchall():
                run = dict(row)
                try:
                    if run.get("parameters"):
                        run["parameters"] = json.loads(run["parameters"])
                    if run.get("results_summary"):
                        run["results_summary"] = json.loads(run["results_summary"])
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse JSON for discovery run ID {run.get('id')}."
                    )
                runs.append(run)
            return runs, total_count

    def get_discovery_run_by_id(self, run_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single discovery run by its ID."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_DISCOVERY_RUN_BY_ID, (run_id,))
            row = cursor.fetchone()
            if row:
                run = dict(row)
                try:
                    if run.get("parameters"):
                        run["parameters"] = json.loads(run["parameters"])
                    if run.get("results_summary"):
                        run["results_summary"] = json.loads(run["results_summary"])
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse JSON for discovery run ID {run.get('id')}."
                    )
                return run
        return None

    def update_discovery_run_log_path(self, run_id: int, log_path: str):
        """Updates the log file path for a discovery run."""
        conn = self._get_conn()
        with conn:
            conn.execute(queries.UPDATE_DISCOVERY_RUN_LOG_PATH, (log_path, run_id))

    def get_keywords_for_run(self, run_id: int) -> List[Dict[str, Any]]:
        """Retrieves all opportunities associated with a specific discovery run ID."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM opportunities WHERE run_id = ?", (run_id,))
            return self._deserialize_rows(cursor.fetchall())

    def get_keywords_for_run_by_reason(
        self, run_id: int, reason: str
    ) -> List[Dict[str, Any]]:
        """Retrieves all opportunities associated with a specific discovery run ID that were disqualified for a specific reason."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_KEYWORDS_FOR_RUN_BY_REASON, (run_id, reason))
            return self._deserialize_rows(cursor.fetchall())

    def search_discovery_runs(self, client_id: str, query: str) -> List[Dict[str, Any]]:
        """Searches for discovery runs by seed keywords or status for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute(
                """
                SELECT id, client_id, start_time, status, parameters, results_summary
                FROM discovery_runs
                WHERE client_id = ? 
                  AND (parameters LIKE ? OR status LIKE ? OR error_message LIKE ?)
                ORDER BY start_time DESC
                LIMIT 10;
            """,
                (client_id, search_term, search_term, search_term),
            )

            runs = []
            for row in cursor.fetchall():
                run = dict(row)
                if run.get("parameters"):
                    run["parameters"] = json.loads(run["parameters"])
                if run.get("results_summary"):
                    run["results_summary"] = json.loads(run["results_summary"])
                runs.append(run)
            return runs

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(queries.GET_JOB, (job_id,))
            row = cursor.fetchone()
            if row:
                job_data = dict(row)
                if job_data.get("result"):
                    job_data["result"] = json.loads(job_data["result"])
                return job_data
        return None

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Retrieves all jobs from the database, ordered by start time."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(queries.GET_ALL_JOBS)
            jobs = []
            for row in cursor.fetchall():
                job_data = dict(row)
                if job_data.get("result"):
                    try:
                        job_data["result"] = json.loads(job_data["result"])
                    except json.JSONDecodeError:
                        job_data["result"] = {"raw_result": job_data["result"]}
                jobs.append(job_data)
            return jobs

    def update_job(self, job_info: Dict[str, Any]):
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_JOB,
                (
                    job_info["id"],
                    job_info.get("client_id"),
                    job_info["status"],
                    job_info["progress"],
                    json.dumps(job_info.get("result")) if job_info.get("result") else None,
                    job_info.get("error"),
                    job_info.get("function_name"),
                    job_info["started_at"],
                    job_info.get("finished_at"),
                ),
            )

    def get_client_prompt_templates(self, client_id: str) -> List[Dict[str, Any]]:
        """MOCK: Retrieves all prompt templates for a client."""
        return []

    def save_client_prompt_template(
        self, client_id: str, template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """MOCK: Saves or updates a client's prompt template."""
        template_data["last_updated"] = datetime.now().isoformat()
        return template_data

    def delete_client_prompt_template(self, client_id: str, template_name: str):
        """MOCK: Deletes a client's prompt template."""
        pass

    def update_opportunity_ai_content_and_status(
        self,
        opportunity_id: int,
        ai_content_data: Dict[str, Any],
        ai_model: str,
        status: str,
    ):
        """Stores the generated AI content package, model, and status used for a specific opportunity."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving AI content generated by model '{ai_model}' and setting status to '{status}'."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_AI_CONTENT_AND_STATUS,
                (
                    json.dumps(ai_content_data),
                    ai_model,
                    datetime.now().isoformat(),
                    status,
                    opportunity_id,
                ),
            )

    def save_content_version_to_history(
        self,
        opportunity_id: int,
        ai_content_json: Dict[str, Any],
        timestamp: Optional[str] = None,
    ):
        """Saves the current content package of an opportunity to the history table."""
        conn = self._get_conn()
        timestamp = timestamp or datetime.now().isoformat()
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving content version to history at {timestamp}."
        )
        with conn:
            conn.execute(
                queries.INSERT_CONTENT_HISTORY,
                (opportunity_id, timestamp, json.dumps(ai_content_json)),
            )

    def save_content_feedback(
        self, opportunity_id: int, rating: int, comments: Optional[str] = None
    ):
        """Saves user feedback for generated content."""
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.INSERT_CONTENT_FEEDBACK,
                (opportunity_id, rating, comments, datetime.now().isoformat()),
            )
        self.logger.info(
            f"Saved content feedback for opportunity {opportunity_id} (Rating: {rating})."
        )

    def get_content_history(self, opportunity_id: int) -> List[Dict[str, Any]]:
        """Retrieves all historical content versions for an opportunity."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_CONTENT_HISTORY_BY_OPP_ID, (opportunity_id,))
            rows = cursor.fetchall()

            results = []
            for row in rows:
                row_dict = dict(row)
                if row_dict.get("ai_content_json"):
                    row_dict["ai_content_json"] = json.loads(
                        row_dict["ai_content_json"]
                    )
                results.append(row_dict)
            return results

    def restore_content_version(
        self, opportunity_id: int, version_timestamp: str
    ) -> Optional[Dict[str, Any]]:
        """
        Restores a content version from history. Before restoring, it saves the current
        'generated' content to the history table to prevent data loss.
        """
        conn = self._get_conn()
        with conn:
            # First, fetch the current opportunity to save its content
            cursor = conn.execute(queries.SELECT_OPPORTUNITY_BY_ID, (opportunity_id,))
            current_opp_row = cursor.fetchone()
            if not current_opp_row:
                self.logger.error(
                    f"Cannot restore: Opportunity {opportunity_id} not found."
                )
                return None

            current_opp = self._deserialize_rows([current_opp_row])[0]
            current_content = current_opp.get("ai_content")

            # Save the current 'generated' content to history before overwriting
            if current_content and current_opp.get("status") == "generated":
                self.save_content_version_to_history(opportunity_id, current_content)

            # Now, find the historical version to restore
            cursor = conn.execute(
                "SELECT ai_content_json FROM content_history WHERE opportunity_id = ? AND timestamp = ?",
                (opportunity_id, version_timestamp),
            )
            version_to_restore_row = cursor.fetchone()

            if (
                not version_to_restore_row
                or not version_to_restore_row["ai_content_json"]
            ):
                self.logger.error(
                    f"Version not found or content missing for timestamp: {version_timestamp}"
                )
                raise ValueError(f"Content version at {version_timestamp} not found.")

            restored_content_str = version_to_restore_row["ai_content_json"]
            restored_content = json.loads(restored_content_str)

            # Update the main opportunities table with the restored content
            conn.execute(
                queries.UPDATE_OPPORTUNITY_AI_CONTENT_AND_STATUS,
                (
                    restored_content_str,
                    current_opp.get(
                        "ai_content_model", "gpt-4o"
                    ),  # Keep the last used model
                    datetime.now().isoformat(),
                    "generated",  # Reset status to 'generated'
                    opportunity_id,
                ),
            )
            self.logger.info(
                f"Successfully restored content from {version_timestamp} for opportunity {opportunity_id}."
            )

        return restored_content

    def update_opportunity_social_posts(
        self, opportunity_id: int, social_media_posts: List[Dict[str, Any]]
    ):
        """Stores the updated social media posts JSON for a specific opportunity."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving updated social media posts."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_OPPORTUNITY_SOCIAL_POSTS,
                (json.dumps(social_media_posts), opportunity_id),
            )

    def update_social_media_posts_status(self, opportunity_id: int, new_status: str):
        """Updates the status of social media posts for an opportunity."""
        self.logger.info(
            f"Opportunity {opportunity_id}: Updating social media posts status to '{new_status}'."
        )
        conn = self._get_conn()
        with conn:
            conn.execute(
                "UPDATE opportunities SET social_media_posts_status = ? WHERE id = ?",
                (new_status, opportunity_id),
            )

    def save_full_content_package(
        self,
        opportunity_id: int,
        ai_content_data: Dict[str, Any],
        ai_model: str,
        featured_image_data: Optional[Dict[str, Any]],
        in_article_images_data: List[Dict[str, Any]],
        social_posts: Optional[List[Dict[str, Any]]],
        final_package: Dict[str, Any],
        total_api_cost: float,
    ):
        """
        Saves the entire generated content package and updates the status to 'generated' in a single transaction.
        Applies server-side sanitization to the main HTML body. (W20 FIX)
        """
        self.logger.info(
            f"Opportunity {opportunity_id}: Saving full content package and finalizing status."
        )

        # W20 FIX: Sanitize the final package HTML content before saving
        html_body = final_package.get("article_html_final")
        if html_body:
            clean_html = bleach.clean(
                html_body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES_DB
            )
            final_package["article_html_final"] = clean_html

        conn = self._get_conn()
        with conn:
            conn.execute(
                queries.UPDATE_GENERATED_CONTENT_AND_STATUS,
                (
                    json.dumps(ai_content_data),
                    ai_model,
                    featured_image_data.get("remote_url")
                    if featured_image_data
                    else None,
                    featured_image_data.get("local_path")
                    if featured_image_data
                    else None,
                    json.dumps(in_article_images_data),
                    json.dumps(social_posts) if social_posts else None,
                    json.dumps(final_package),
                    datetime.now().isoformat(),
                    total_api_cost,
                    opportunity_id,
                ),
            )
        self.logger.info(
            f"Opportunity {opportunity_id}: Successfully saved full content package and set status to 'generated'."
        )

        def update_opportunity_published_url(self, opportunity_id: int, url: str):
            """Updates the published_url for a specific opportunity."""
            self.logger.info(
                f"Opportunity {opportunity_id}: Storing published URL: {url}"
            )
            conn = self._get_conn()
            with conn:
                conn.execute(
                    "UPDATE opportunities SET published_url = ? WHERE id = ?",
                    (url, opportunity_id),
                )

    def get_high_priority_opportunities(
        self, client_id: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieves the top N validated opportunities with the highest strategic score."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                queries.SELECT_HIGH_PRIORITY_OPPORTUNITIES, (client_id, limit)
            )
            return self._deserialize_rows(cursor.fetchall())

    def get_content_feedback_examples(
        self, client_id: str, limit: int = 2
    ) -> Dict[str, List]:
        """Retrieves examples of good and bad content based on user feedback."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()

            # Get highest rated
            cursor.execute(
                """
                SELECT o.keyword, cf.comments, cf.rating
                FROM content_feedback cf
                JOIN opportunities o ON cf.opportunity_id = o.id
                WHERE o.client_id = ? AND cf.rating >= 4
                ORDER BY cf.rating DESC, cf.timestamp DESC
                LIMIT ?;
            """,
                (client_id, limit),
            )
            good_examples = [dict(row) for row in cursor.fetchall()]

            # Get lowest rated
            cursor.execute(
                """
                SELECT o.keyword, cf.comments, cf.rating
                FROM content_feedback cf
                JOIN opportunities o ON cf.opportunity_id = o.id
                WHERE o.client_id = ? AND cf.rating <= 2
                ORDER BY cf.rating ASC, cf.timestamp DESC
                LIMIT ?;
            """,
                (client_id, limit),
            )
            bad_examples = [dict(row) for row in cursor.fetchall()]

        return {"good_examples": good_examples, "bad_examples": bad_examples}

    def get_qualification_settings(self, client_id: str) -> Dict[str, Any]:
        """Retrieves qualification settings for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM qualification_settings WHERE client_id = ?", (client_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {}

    def get_qualification_strategies(self, client_id: str) -> List[Dict[str, Any]]:
        """Retrieves all qualification strategies for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM qualification_strategies WHERE client_id = ?",
                (client_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_qualification_strategy_by_id(
        self, strategy_id: int
    ) -> Optional[Dict[str, Any]]:
        """Retrieves a single qualification strategy by its ID."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM qualification_strategies WHERE id = ?", (strategy_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def create_qualification_strategy(
        self, client_id: str, strategy: Dict[str, Any]
    ) -> int:
        """Creates a new qualification strategy for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            keys = ", ".join(strategy.keys())
            placeholders = ", ".join("?" * len(strategy))
            values = list(strategy.values())
            cursor.execute(
                f"INSERT INTO qualification_strategies (client_id, {keys}) VALUES (?, {placeholders})",
                [client_id] + values,
            )
            return cursor.lastrowid

    def update_qualification_strategy(self, strategy_id: int, strategy: Dict[str, Any]):
        """Updates a qualification strategy."""
        conn = self._get_conn()
        with conn:
            set_clauses = []
            values = []
            for key, value in strategy.items():
                set_clauses.append(f"{key} = ?")
                values.append(value)

            if set_clauses:
                update_query = f"UPDATE qualification_strategies SET {', '.join(set_clauses)} WHERE id = ?"
                values.append(strategy_id)
                conn.execute(update_query, values)

    def delete_qualification_strategy(self, strategy_id: int):
        """Deletes a qualification strategy."""
        conn = self._get_conn()
        with conn:
            conn.execute(
                "DELETE FROM qualification_strategies WHERE id = ?", (strategy_id,)
            )

    def update_qualification_settings(self, client_id: str, settings: Dict[str, Any]):
        """Updates qualification settings for a specific client."""
        conn = self._get_conn()
        with conn:
            set_clauses = []
            values = []
            for key, value in settings.items():
                set_clauses.append(f"{key} = ?")
                values.append(value)

            if set_clauses:
                update_query = f"UPDATE qualification_settings SET {', '.join(set_clauses)} WHERE client_id = ?"
                values.append(client_id)
                conn.execute(update_query, values)

    def get_content_snippet_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Retrieves the title and a content snippet for an opportunity by its slug."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(
                """
                SELECT keyword as title,
                       SUBSTR(JSON_EXTRACT(ai_content_json, '$.meta_description'), 1, 200) as snippet_desc
                FROM opportunities WHERE slug = ?;
            """,
                (slug,),
            )

    def get_active_jobs_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        """Retrieves all jobs with 'running' or 'pending' status for a client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(queries.GET_ACTIVE_JOBS_BY_CLIENT, (client_id,))
            jobs = []
            for row in cursor.fetchall():
                job_data = dict(row)
                if job_data.get("result"):
                    try:
                        job_data["result"] = json.loads(job_data["result"])
                    except json.JSONDecodeError:
                        job_data["result"] = {"raw_result": job_data["result"]}
                jobs.append(job_data)
            return jobs
            row = cursor.fetchone()
            if row:
                return dict(row)
        return None

    def fail_stale_jobs(self):
        """Finds all jobs with a 'running' status and marks them as 'failed' on startup."""
        self.logger.info("Scanning for stale jobs from previous sessions...")
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            error_message = "Job failed due to application restart."
            finished_time = time.time()
            cursor.execute(
                """
                UPDATE jobs
                SET status = 'failed', error = ?, finished_at = ?
                WHERE status = 'running';
            """,
                (error_message, finished_time),
            )

            if cursor.rowcount > 0:
                self.logger.warning(
                    f"Marked {cursor.rowcount} stale 'running' jobs as 'failed'."
                )
            else:
                self.logger.info("No stale jobs found.")

        def override_disqualification(self, opportunity_id: int) -> bool:
            """Manually overrides a failed qualification, resetting status to pending."""
            self.logger.info(
                f"Overriding disqualification for opportunity ID: {opportunity_id}"
            )
            conn = self._get_conn()
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE opportunities
                    SET status = 'pending', blog_qualification_status = 'passed_manual_override', blog_qualification_reason = 'Manually overridden by user.'
                    WHERE id = ? AND status IN ('failed', 'rejected');
                """,
                    (opportunity_id,),
                )

                if cursor.rowcount > 0:
                    self.logger.info(
                        f"Successfully overrode disqualification for opportunity ID: {opportunity_id}"
                    )
                    return True
                else:
                    self.logger.warning(
                        f"Could not override disqualification for ID: {opportunity_id}. Status was not 'failed' or 'rejected'."
                    )
                    return False