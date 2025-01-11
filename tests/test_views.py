from unittest.mock import Mock, patch

from src.views import cards_total_spent, get_currency_rates, get_stock_prices, get_top_transactions


# ТЕСТ PASSED
def test_cards_total_spent(filtered_by_dates_df, cards_spent) -> None:
    """ Тест на правильность подсчета сумм по каждой карте и расчет кэшбека. """
    dict_ = filtered_by_dates_df.to_dict(orient="records")
    assert cards_total_spent(dict_) == cards_spent


# ТЕСТ PASSED
def test_get_top_transactions(filtered_by_dates_df, top_5_expences) -> None:
    """ Тест на правильность выборки топ 5 транзакций. """
    dict_ = filtered_by_dates_df.to_dict(orient="records")
    assert get_top_transactions(dict_) == top_5_expences


# ТЕСТ PASSED
@patch('requests.get')
@patch('os.getenv')
def test_get_currency_rates(mocked_os, mocked_get, currencies_list, currencies_to_get) -> None:
    """ Тест на случай успешного запроса курса валют. """
    mocked_os.return_value = 'abc123'
    mocked_get.return_value.status_code = 200
    mock_json = Mock(side_effect=[{"info": {"rate": 73.21}}, {"info": {"rate": 87.08}}])
    mocked_get.return_value.json.side_effect = mock_json.side_effect

    assert get_currency_rates(currencies_list) == currencies_to_get


# ТЕСТ PASSED
@patch('requests.get')
@patch('os.getenv')
def test_get_currency_rates_fail_response(mocked_os, mocked_get, currencies_list, currencies_to_get) -> None:
    """ Тест на случай получения неуспешного запроса курса валют. """
    mocked_os.return_value = 'abc123'
    mocked_get.return_value.status_code = 400

    assert get_currency_rates(currencies_list) == [{"currency": "USD", "rate": "N/A"},
                                                   {"currency": "EUR", "rate": "N/A"}]


# ТЕСТ PASSED
@patch('requests.get')
@patch('os.getenv')
def test_get_stock_prices(mocked_os, mocked_get, stocks_list, stocks_to_get) -> None:
    """ Тест на случай успешного запроса цен на акции. """
    mocked_os.return_value = 'abc123'
    mocked_get.return_value.status_code = 200
    mock_json = Mock(side_effect=[{"data": [{"close": 150.12}]}, {"data": [{"close": 3173.18}]}])
    mocked_get.return_value.json.side_effect = mock_json.side_effect

    assert get_stock_prices(stocks_list) == stocks_to_get


# ТЕСТ PASSED
@patch('requests.get')
@patch('os.getenv')
def test_get_stock_prices_fail_response(mocked_os, mocked_get, stocks_list, stocks_to_get) -> None:
    """ Тест на случай получения неуспешного запроса цен на акции. """
    mocked_os.return_value = 'abc123'
    mocked_get.return_value.status_code = 400

    assert get_stock_prices(stocks_list) == []
