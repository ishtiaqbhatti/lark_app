import os
import configparser
from dotenv import load_dotenv
import json # NEW import
from typing import Dict, Any, List, Optional
import logging


class ConfigManager:
    # Force reload
    _setting_types = {
        # ... (existing types) ...
        "filters_json": list,  # NEW: Add this for goal-specific filters (JSON parsed to list)
        "discovery_goals": list,  # NEW: Add this
        "default_sv": int, # NEW: Add for goal presets
        "default_kd": int, # NEW: Add for goal presets
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
        "default_multiplier": float,
        "comprehensive_article": float,
        "how_to_guide": float,
        "comparison_post": float,
        "review_article": float,
        "video_led_article": float,
        "forum_summary_post": float,
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
        "load_async_ai_overview": bool,
        "onpage_check_spell": bool,
        "disable_ai_overview_check": bool,
        "onpage_enable_switch_pool": bool,
        "onpage_enable_custom_js": bool,
        "discovery_exact_match": bool,
        "onpage_browser_screen_resolution_ratio": float, # Keep this in floats section
        # NEW: Add custom prompt template
        "custom_prompt_template": str,
        "expert_persona": str, # string in client settings
        "client_knowledge_base": str, # string in client settings
        "brand_tone": str, # string in client settings
        "target_audience": str, # string in client settings
        "terms_to_avoid": str, # string in client settings
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
        """Configures logging to file and console."""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(log_dir, "app.log")),
                logging.StreamHandler()
            ]
        )


    def _get_list_from_config(
        self, section: str, key: str, fallback: Optional[str] = None
    ) -> List[str]:
        try:
            value_str = self.config_parser.get(section, key)
            return [item.strip() for item in value_str.split(",") if item.strip()]
        except (configparser.NoOptionError, configparser.NoSectionError):
            return [item.strip() for item in (fallback or "").split(",") if item.strip()]


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
                        if key.endswith("_json") or key == "filters_json": # NEW: Handle filters_json
                            try:
                                settings[key] = json.loads(value)
                            except json.JSONDecodeError:
                                self.logger.error(f"Failed to parse JSON for key [{section}]{key}. Value: '{value}'. Setting to empty list.")
                                settings[key] = []
                        else:
                            settings[key] = self._get_list_from_config(section, key)
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
                "filters_json", # NEW: Goal presets are globally managed.
                "discovery_goals", # NEW: Goal list is globally managed.
                "default_sv", # NEW: Goal defaults are globally managed.
                "default_kd", # NEW: Goal defaults are globally managed.
            ]
        )

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
                        if key.endswith("_json") or key == "filters_json": # NEW: Handle JSON lists
                            self.config_parser.set(
                                section, key, json.dumps(updated_global_settings[key])
                            )
                        else:
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

    def get_goal_preset_config(self, goal_name: str) -> Dict[str, Any]:
        """
        Retrieves the filter and order_by presets for a given discovery goal.
        """
        # Sanitize goal_name to match the INI section format, e.g., "Find Low-Hanging Fruit" -> "DISCOVERY_GOAL_LOW_HANGING_FRUIT"
        sanitized_goal_name = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in goal_name)
        section_name = f"DISCOVERY_GOAL_{sanitized_goal_name.replace(' ', '_').upper()}"
        
        # Find the closest match in the config parser sections
        closest_section_name = next((s for s in self.config_parser.sections() if section_name in s), None)

        if not closest_section_name:
            self.logger.error(f"Goal preset section matching '{section_name}' not found in settings.ini.")
            return {}
        
        goal_settings = {}
        for key, value in self.config_parser.items(closest_section_name):
            try:
                if key == "filters_json":
                    goal_settings["filters"] = json.loads(value)
                elif key == "order_by":
                    goal_settings["order_by"] = [item.strip() for item in value.split('|') if item.strip()]
                elif key == "default_sv":
                    goal_settings["default_sv"] = int(value)
                elif key == "default_kd":
                    goal_settings["default_kd"] = int(value)
                else:
                    goal_settings[key] = value
            except (json.JSONDecodeError, ValueError) as e:
                self.logger.error(f"Error parsing goal preset '{key}' for goal '{goal_name}': {e}")
                
        return goal_settings
