import pytest
from unittest.mock import patch, MagicMock
from src.llm_blocks.customize_json_data import customize_json_data


@pytest.fixture
def sample_input():
    return {
        "business_name": "EcoFresh Solutions",
        "business_description": "An eco-friendly company providing sustainable cleaning products.",
        "json_placeholder": {
            "C001": "Meta description",
            "C002": "Page title",

            "C003": "Main menu link 1 (Home)",
            "C004": "Main menu link 2 (Process)",
            "C005": "Main menu link 3 (Services)",
            "C006": "Main menu link 4 (About)",
            "C007": "Main menu link 5 (Pricing)",
            "C008": "Main menu link 6 (Blog)",
            "C009": "Nav button text (e.g. Start Writing)",
            "C010": "Footer text"  }
    }


def test_customize_json_data_returns_expected_dict(sample_input):
    
    result = customize_json_data(
        sample_input["business_name"],
        sample_input["business_description"],
        sample_input["json_placeholder"]
    )
    
    assert isinstance(result, dict)

