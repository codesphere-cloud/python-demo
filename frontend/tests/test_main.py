import pytest
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Any

from main import calculate_summary_stats

@dataclass
class Case:
    name: str
    input_df: pd.DataFrame
    expected_output: Dict[str, Any]

TEST_SCENARIOS: List[Case] = [
    Case(
        name="base case with positive values",
        input_df=pd.DataFrame({
            'A': [1, 2, 3, 6],  
            'B': [10, 5, 20, 1] 
        }),
        expected_output={'mean_A': 3.0, 'max_B': 20.0, 'total_points': 4}
    ),
    Case(
        name="edge case: empty DataFrame",
        input_df=pd.DataFrame({'A': [], 'B': []}),
        expected_output={'mean_A': 0, 'max_B': 0, 'total_points': 0}
    ),
    Case(
        name="base case with negative values",
        input_df=pd.DataFrame({
            'A': [-10, 0, 10],   
            'B': [-5, -1, -100]  
        }),
        expected_output={'mean_A': 0.0, 'max_B': -1.0, 'total_points': 3}
    ),
    Case(
        name="case with only one data point.",
        input_df=pd.DataFrame({'A': [100], 'B': [500]}),
        expected_output={'mean_A': 100.0, 'max_B': 500.0, 'total_points': 1}
    ),
]

@pytest.mark.parametrize(
    "scenario",
    TEST_SCENARIOS,
    ids=[s.name for s in TEST_SCENARIOS] 
)
def test_calculate_summary_stats(scenario: Case):
    result = calculate_summary_stats(scenario.input_df)
    assert result == pytest.approx(scenario.expected_output)