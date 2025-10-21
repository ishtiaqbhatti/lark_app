# tests/test_filter_transformation.py
from pipeline.step_01_discovery.keyword_discovery.expander import (
    _transform_filters_for_api,
)


def test_no_filters():
    """Test that None is returned when no filters are provided."""
    assert _transform_filters_for_api(None) is None


def test_single_filter():
    """Test that a single filter is transformed into a flat list."""
    filters = [{"field": "keyword_info.search_volume", "operator": ">", "value": 100}]
    expected = ["keyword_info.search_volume", ">", 100]
    assert _transform_filters_for_api(filters) == expected


def test_multiple_filters():
    """Test that multiple filters are correctly interleaved with the 'and' operator."""
    filters = [
        {"field": "keyword_info.search_volume", "operator": ">", "value": 100},
        {
            "field": "keyword_properties.keyword_difficulty",
            "operator": "<",
            "value": 50,
        },
    ]
    expected = [
        ["keyword_info.search_volume", ">", 100],
        "and",
        ["keyword_properties.keyword_difficulty", "<", 50],
    ]
    assert _transform_filters_for_api(filters) == expected


def test_three_filters():
    """Test that three filters are correctly interleaved with the 'and' operator."""
    filters = [
        {"field": "keyword_info.search_volume", "operator": ">", "value": 100},
        {
            "field": "keyword_properties.keyword_difficulty",
            "operator": "<",
            "value": 50,
        },
        {"field": "keyword_info.cpc", "operator": ">", "value": 0.5},
    ]
    expected = [
        ["keyword_info.search_volume", ">", 100],
        "and",
        ["keyword_properties.keyword_difficulty", "<", 50],
        "and",
        ["keyword_info.cpc", ">", 0.5],
    ]
    assert _transform_filters_for_api(filters) == expected


def test_empty_filter_list():
    """Test that an empty list of filters returns None."""
    assert _transform_filters_for_api([]) is None
