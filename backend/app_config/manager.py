import os
import configparser
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
import logging


class ConfigManager:
    """
    Manages loading, validating, and providing configuration settings.
    Handles global defaults from settings.ini and client-specific overrides.
    """

    _setting_types = {
        # Integers
        "location_code": int,
        "max_sv_for_scoring": int,
        "max_domain_rank_for_scoring": int,
        "max_referring_domains_for_scoring": int,
        "max_avg_referring_domains_filter": int,
        "serp_freshness_old_threshold_days": int,
        "serp_volatility_stable_threshold_days": int,
        "min_competitor_word_count": int,
        "max_competitor_technical_warnings": int,
        "num_competitors_to_analyze": int,
        "num_common_headings": int,
        "num_unique_angles": int,
        "max_initial_serp_urls_to_analyze": int,
        "people_also_ask_click_depth": int,
        "min_search_volume": int,
        "max_keyword_difficulty": int,
        "num_in_article_images": int,
        "onpage_max_domains_per_request": int,
        "onpage_max_tasks_per_request": int,
        "deep_dive_top_n_keywords": int,
        "max_tokens_for_generation": int,
        "discovery_max_pages": int,
        "min_serp_results": int,
        "max_serp_results": int,
        "min_avg_backlinks": int,
        "max_avg_backlinks": int,
        "discovery_related_depth": int,
        "yearly_trend_decline_threshold": int,
        "quarterly_trend_decline_threshold": int,
        "max_kd_hard_limit": int,
        "max_referring_main_domains_limit": int,
        "max_avg_domain_rank_threshold": int,
        "min_keyword_word_count": int,
        "max_keyword_word_count": int,
        "crowded_serp_features_threshold": int,
        "min_serp_stability_days": int,
        "max_non_blog_results": int,
        "max_ai_overview_words": int,
        "max_first_organic_y_pixel": int,
        "max_words_for_ai_analysis": int,
        "num_competitors_for_ai_analysis": int,
        "max_avg_lcp_time": int,  # NEW
        "high_value_sv_override_threshold": int,
        "overlay_font_size": int,
        # Floats
        "informational_score": float,
        "commercial_score": float,
        "transactional_score": float,
        "navigational_score": float,
        "question_keyword_bonus": float,
        "max_cpc_for_scoring": float,
        "featured_snippet_bonus": float,
        "ai_overview_bonus": float,
        "serp_freshness_bonus_max": float,
        "min_cpc_filter": float,
        "min_yearly_trend_filter": float,
        "min_cpc": float,
        "max_cpc": float,
        "min_competition": float,
        "max_competition": float,
        "min_cpc_filter_api": float,
        "category_intent_bonus": float,
        "search_volume_volatility_threshold": float,
        "max_paid_competition_score": float,
        "max_high_top_of_page_bid": float,
        "max_pages_to_domain_ratio": float,
        "ai_generation_temperature": float,
        "recommended_word_count_multiplier": float,
        "default_multiplier": float,  # ADDED
        "comprehensive_article": float,  # ADDED
        "how_to_guide": float,  # ADDED
        "comparison_post": float,  # ADDED
        "review_article": float,  # ADDED
        "video_led_article": float,  # ADDED
        "forum_summary_post": float,  # ADDED
        "recipe_article": float,
        "scholarly_summary": float,
        "product_comparison": float,
        "high_value_cpc_override_threshold": float,
        # Booleans
        "require_question_keywords": bool,
        "enforce_intent_filter": bool,
        "calculate_rectangles": bool,
        "enable_cache": bool,
        "deep_dive_discovery": bool,
        "use_pexels_first": bool,
        "cleanup_local_images": bool,
        "onpage_enable_javascript": bool,
        "onpage_load_resources": bool,
        "onpage_disable_cookie_popup": bool,
        "onpage_return_despite_timeout": bool,
        "onpage_enable_browser_rendering": bool,
        "onpage_store_raw_html": bool,
        "onpage_validate_micromarkup": bool,
        "discovery_replace_with_core_keyword": bool,
        "discovery_ignore_synonyms": bool,
        "enable_automated_internal_linking": bool,
        "generate_toc": bool,
        "overlay_text_enabled": bool,
        "include_clickstream_data": bool,
        "load_async_ai_overview": bool,  # ADD THIS FOR W3
        "onpage_check_spell": bool,  # ADD THIS LINE (W5 FIX)
        "disable_ai_overview_check": bool,
        "onpage_accept_language": str,  # ADD THIS LINE (W7 FIX)
        "onpage_enable_switch_pool": bool,  # ADD THIS LINE (W13 FIX)
        "onpage_enable_custom_js": bool,  # ADD THIS LINE (W12 FIX)
        "onpage_custom_js": str,  # ADD THIS LINE (W12 FIX)
        "discovery_exact_match": bool,  # ADD THIS LINE (W7 FIX)
        "onpage_browser_screen_resolution_ratio": float,  # ADD THIS LINE (W7 FIX)
        # Lists (comma-separated strings)
        "allowed_intents": list,
        "negative_keywords": list,
        "competitor_blacklist_domains": list,
        "serp_feature_filters": list,
        "serp_features_exclude_filter": list,
        "platforms": list,
        "default_wordpress_categories": list,
        "default_wordpress_tags": list,
        "ugc_and_parasite_domains": list,
        "high_value_categories": list,
        "hostile_serp_features": list,
        "final_validation_non_blog_domains": list,
        # Weights
        "ease_of_ranking_weight": float,
        "traffic_potential_weight": float,
        "commercial_intent_weight": float,
        "serp_features_weight": float,
        "growth_trend_weight": float,
        "serp_freshness_weight": float,
        "serp_volatility_weight": float,
        "competitor_weakness_weight": float,
        "competitor_performance_weight": float,  # ADDED THIS LINE
        # Strings
        "max_competition_level": str,
        "non_evergreen_year_pattern": str,
        "db_file_name": str,  # NEW
        "db_type": str,  # NEW
        "overlay_text_color": str,
        "overlay_background_color": str,
        "overlay_position": str,
        "closely_variants": bool,
        "max_cpc_filter": float,
        "discovery_order_by_field": str,
        "discovery_order_by_direction": str,
        "search_phrase_regex": str,
        "onpage_custom_checks_thresholds": str,  # ADD THIS LINE (W9 FIX)
        "serp_remove_from_url_params": str,
        "schema_author_type": str,
        "client_knowledge_base": str,
        "wordpress_url": str,
        "wordpress_user": str,
        "wordpress_app_password": str,
        "wordpress_seo_plugin": str,
    }

    def __init__(self, settings_path: str = "backend/app_config/settings.ini"):
        load_dotenv()
        self.config_parser = configparser.ConfigParser(inline_comment_prefixes=(";",))
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Configuration file not found at: {settings_path}")
        self.config_parser.read(settings_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._configure_logging()
        self._global_settings = self._load_and_validate_global()

    def _configure_logging(self):
        """Sets up basic logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        self.logger.info("Logging configured.")

    def _get_int_from_config(
        self, section: str, key: str, fallback: Optional[int] = None
    ) -> int:
        try:
            value_str = self.config_parser.get(section, key)
            return int(value_str)
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
            if fallback is not None:
                return fallback
            raise ValueError(
                f"Missing or invalid integer configuration for [{section}]{key}"
            )

    def _get_float_from_config(
        self, section: str, key: str, fallback: Optional[float] = None
    ) -> float:
        try:
            value_str = self.config_parser.get(section, key)
            return float(value_str)
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
            if fallback is not None:
                return fallback
            raise ValueError(
                f"Missing or invalid float configuration for [{section}]{key}"
            )

    def _get_list_from_config(
        self, section: str, key: str, fallback: str = ""
    ) -> List[str]:
        try:
            value_str = self.config_parser.get(section, key)
            return [item.strip() for item in value_str.split(",") if item.strip()]
        except (configparser.NoOptionError, configparser.NoSectionError):
            return [item.strip() for item in fallback.split(",") if item.strip()]

    def _load_and_validate_global(self) -> Dict[str, Any]:
        """Loads all global settings from settings.ini and .env."""
        settings = {}

        # API Credentials (from .env)
        settings["dataforseo_login"] = os.getenv("DATAFORSEO_LOGIN")
        settings["dataforseo_password"] = os.getenv("DATAFORSEO_PASSWORD")
        if not settings["dataforseo_login"] or not settings["dataforseo_password"]:
            self.logger.critical(
                "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set in the .env file."
            )
            raise ValueError(
                "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set in the .env file."
            )

        settings["openai_api_key"] = os.getenv("OPENAI_API_KEY")
        if not settings["openai_api_key"]:
            self.logger.warning(
                "OPENAI_API_KEY is not set in the .env file. AI content generation will likely fail."
            )

        settings["pexels_api_key"] = os.getenv("PEXELS_API_KEY")
        if not settings["pexels_api_key"]:
            self.logger.warning(
                "PEXELS_API_KEY is not set in the .env file. Pexels integration will be unavailable."
            )

        # UI Password (from .env)
        settings["ui_password"] = os.getenv("UI_PASSWORD")
        if not settings["ui_password"]:
            self.logger.critical(
                "UI_PASSWORD must be set in the .env file for Streamlit authentication."
            )
            raise ValueError("UI_PASSWORD must be set in the .env file.")

        # Load all settings from settings.ini
        for section in self.config_parser.sections():
            for key, value in self.config_parser.items(section):
                try:
                    target_type = self._setting_types.get(key)
                    if target_type is bool:
                        settings[key] = self.config_parser.getboolean(section, key)
                    elif target_type is int:
                        settings[key] = self.config_parser.getint(section, key)
                    elif target_type is float:
                        settings[key] = self.config_parser.getfloat(section, key)
                    elif target_type is list:
                        raw_values = self._get_list_from_config(section, key)
                        if key == "serp_feature_filters":
                            parsed_filters = []
                            for f_str in raw_values:
                                if f_str.startswith("no_"):
                                    parsed_filters.append(
                                        {"type": "has_not", "feature": f_str[3:]}
                                    )
                                elif f_str.startswith("has_"):
                                    parsed_filters.append(
                                        {"type": "has", "feature": f_str[4:]}
                                    )
                            settings[key] = parsed_filters
                        else:
                            settings[key] = raw_values
                    else:  # Default to string if no type is mapped
                        settings[key] = value
                except Exception as e:
                    self.logger.critical(
                        f"FATAL CONFIG ERROR: Could not parse key [{section}]{key} with value '{value}' to expected type: {e}"
                    )
                    raise ValueError(
                        f"Configuration key parsing failed for [{section}]{key}. Value: '{value}'."
                    )

        self.logger.info("Global settings loaded.")
        return settings

    def get_global_config(self) -> Dict[str, Any]:
        """Returns the loaded global configuration."""
        return self._global_settings

    def get_default_client_settings_template(self) -> Dict[str, Any]:
        """Returns a template of client settings based on global config, for new client creation."""
        template = self._global_settings.copy()
        template.pop("dataforseo_login", None)
        template.pop("dataforseo_password", None)
        template.pop("openai_api_key", None)
        template.pop("pexels_api_key", None)
        template.pop("ui_password", None)

        for key, value in template.items():
            if isinstance(value, list):
                template[key] = value[:]
        return template

    def load_client_config(self, client_id: str, db_manager: Any) -> Dict[str, Any]:
        """
        Loads client-specific settings from the database and merges them with global settings.
        Scoring weights are always loaded from the global settings to ensure consistency.
        """
        client_settings_from_db = db_manager.get_client_settings(client_id)
        overridden_settings = self._global_settings.copy()

        # Define keys that should NOT be overridden by client-specific settings to ensure they are globally managed.
        globally_managed_keys = set(
            [
                "dataforseo_login",
                "dataforseo_password",
                "openai_api_key",
                "pexels_api_key",
                "ui_password",
                "db_file_name",
                "cache_file_name",
                "default_client_id",
                "db_type",
            ]
        )  # UPDATED

        for key, value in client_settings_from_db.items():
            if key in globally_managed_keys:
                continue  # Skip override for globally managed keys

            if value is not None and value != "":
                overridden_settings[key] = value

        self.logger.info(f"Loaded client-specific configuration for '{client_id}'.")
        return overridden_settings

    def save_client_settings(
        self, client_id: str, new_settings: Dict[str, Any], db_manager: Any
    ):
        """Saves specified client settings to the database."""
        db_manager.update_client_settings(client_id, new_settings)
        self.logger.info(f"Client settings for '{client_id}' saved to database.")

    def save_global_settings_to_file(self, updated_global_settings: Dict[str, Any]):
        """Saves specified settings back to the settings.ini file (for global defaults)."""
        for section in self.config_parser.sections():
            for key in self.config_parser.options(section):
                if (
                    key in updated_global_settings
                    and updated_global_settings[key] is not None
                ):
                    if isinstance(updated_global_settings[key], list):
                        self.config_parser.set(
                            section, key, ",".join(updated_global_settings[key])
                        )
                    elif isinstance(updated_global_settings[key], bool):
                        self.config_parser.set(
                            section, key, str(updated_global_settings[key]).lower()
                        )
                    else:
                        self.config_parser.set(
                            section, key, str(updated_global_settings[key])
                        )

        with open("backend/app_config/settings.ini", "w") as configfile:
            self.config_parser.write(configfile)

        self._global_settings = self._load_and_validate_global()
        self.logger.info("Global settings updated and reloaded from settings.ini.")
