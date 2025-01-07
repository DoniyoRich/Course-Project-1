from pathlib import Path

import pandas as pd
import pytest

tests_path = str(Path(__file__).parent)


@pytest.fixture
def source_dataframe():
    print(tests_path + r'\test_operations.xlsx')
    return pd.read_excel(tests_path + r'\test_operations.xlsx')


@pytest.fixture
def filtered_by_dates_df():
    return pd.read_excel(tests_path + r'\expected_filtered_by_dates.xlsx').to_dict(orient="records")
