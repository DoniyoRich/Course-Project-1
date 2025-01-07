from datetime import datetime

import pandas as pd
import pytest

from src.utils import greeting, filter_by_dates


@pytest.mark.parametrize(
    'date_, greet', [
        (datetime(2021, 12, 30, 19, 27, 7), 'Добрый вечер'),
        (datetime(2021, 12, 30, 11, 27, 4), 'Доброе утро'),
        (datetime(2021, 12, 30, 15, 27, 2), 'Добрый день'),
        (datetime(2021, 12, 30, 3, 27, 1), 'Доброй ночи')
    ]
)
def test_greeting(date_: datetime, greet: str) -> None:
    assert greeting(date_) == greet


def test_filter_by_dates(source_dataframe: pd.DataFrame, filtered_by_dates_df: pd.DataFrame) -> None:
    start_date = datetime(2021, 10, 1, 0, 0, 0)
    current_date = datetime(2021, 10, 8, 8, 24, 0)
    assert filter_by_dates(source_dataframe, start_date, current_date) == filtered_by_dates_df
    # pd.testing.assert_series_equal(pd.DataFrame(filter_by_dates(source_dataframe, start_date, current_date)), filtered_by_dates_df)

# def test_df():
#     df1=pd.DataFrame({'a':[1,2,3,4,5]})
#     df2=pd.DataFrame({'a':[6,7,8,9,11]})
#
#     expected_res=pd.Series([7,9,11,13,16])
#     pd.testing.assert_series_equal((df1['a']+df2['a']),expected_res,check_names=False)

# import pandas as pd
# pd.testing.assert_frame_equal(spending_by_category(sample_df, "Переводы", date="31.10.2024"), df_by_category)
# assert_frame_equal(mock_obj.call_args.args[0]['first_dict_key_which_points_to_a_df'], expected_df)
