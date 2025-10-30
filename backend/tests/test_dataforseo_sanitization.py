# CREATE NEW FILE: backend/tests/test_dataforseo_sanitization.py

import pytest
import json
from backend.data_mappers.dataforseo_mapper import DataForSEOMapper


class TestDataForSEOSanitization:
    """Test suite for DataForSEO API response sanitization."""
    
    def test_se_results_count_string_to_int_conversion(self):
        """
        Test that se_results_count is converted from string to int.
        Per API docs: Keyword Ideas/Suggestions return this as string.
        """
        serp_info = {
            "se_type": "google",
            "se_results_count": "19880000000",  # String from API
            "serp_item_types": ["organic"],
            "last_updated_time": "2024-07-15 00:43:34 +00:00"
        }
        
        sanitized = DataForSEOMapper._sanitize_serp_info(serp_info)
        
        assert isinstance(sanitized["se_results_count"], int)
        assert sanitized["se_results_count"] == 19880000000
    
    def test_se_results_count_already_int(self):
        """Test that integer se_results_count is preserved."""
        serp_info = {
            "se_type": "google",
            "se_results_count": 115000000,  # Already int (Related Keywords)
            "serp_item_types": ["organic"]
        }
        
        sanitized = DataForSEOMapper._sanitize_serp_info(serp_info)
        
        assert isinstance(sanitized["se_results_count"], int)
        assert sanitized["se_results_count"] == 115000000
    
    def test_se_results_count_invalid_string(self):
        """Test handling of non-numeric
