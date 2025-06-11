import pytest
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Type, Dict, Any
from app import create_data

@dataclass
class Case:
    name: str
    input_points: int
    expected_exception: Optional[Type[Exception]] = None

TEST_CASES: List[Case] = [
    Case(
        name="positiv case: 10 data points",
        input_points=10
    ),
    Case(
        name="edge case: 0 data points",
        input_points=0
    ),
    Case(
        name="negative case: -1 data points (expected ValueError)",
        input_points=-1,
        expected_exception=ValueError
    ),
    Case(
        name="positive case: 1 data point",
        input_points=1
    ),
]

@pytest.mark.parametrize(
    "test_case",
    TEST_CASES,
    ids=[tc.name for tc in TEST_CASES] 
)
def test_create_data(test_case: Case):
    if test_case.expected_exception:
        with pytest.raises(test_case.expected_exception):
            create_data(points=test_case.input_points)
        return

    result = create_data(points=test_case.input_points)

    assert isinstance(result, dict)
    assert 'index' in result
    assert 'columns' in result
    assert 'data' in result

    assert result['columns'] == ['A', 'B']
    assert len(result['index']) == test_case.input_points
    assert len(result['data']) == test_case.input_points

    if test_case.input_points > 0:
        assert isinstance(result['data'][0], list)
        assert len(result['data'][0]) == 2

