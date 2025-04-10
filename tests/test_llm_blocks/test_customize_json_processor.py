import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.llm_blocks.custmize_json_placeholder import CustomizeJsonPlaceholder
from src.llm_blocks_helper.api_key_loader import APIKeyLoader
from src.llm_blocks_helper.model_loader import ModelLoader
from src.llm_blocks_helper.prompt_loader import PromptLoader
from src.llm_blocks_helper.chain_builder import ChainBuilder


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
            "C010": "Footer text"  },
        
        "images_description": 
            {
            "assets/img/100x100/1.png": "A person wearing glasses and a black t-shirt. They have a friendly expression and are smiling. The background is plain white."  ,
            "assets/img/100x100/2.png": "A person wearing a dark-colored shirt with a mandarin collar. The background is plain and light-colored, emphasizing the subject's face."  
                }
    }

api_key_loader = APIKeyLoader()
model_loader = ModelLoader()
prompt_loader = PromptLoader()
chain_builder = ChainBuilder()

def test_customize_json_data_returns_expected_dict(sample_input):
    processor = CustomizeJsonPlaceholder(
                            api_key_loader=api_key_loader,
                            model_loader=model_loader,
                            prompt_loader=prompt_loader,
                            chain_builder=chain_builder
                                )
    
    result = processor.run(
        sample_input["business_name"],
        sample_input["business_description"],
        sample_input["images_description"],
        sample_input["json_placeholder"]
    )
    
    assert isinstance(result, dict)

