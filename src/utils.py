from typing import Any

import pandas as pd
from black import datetime
from pandas import DataFrame


def greeting(date_: datetime) -> str:
    """
    Функция принимает текущую дату со временем и возвращает приветствие
    в зависимости от времени суток.
    """
    hour = date_.hour
    message = "Доброе утро"
    if 12 <= hour < 18:
        message = "Добрый день"
    elif 18 <= hour <= 23:
        message = "Добрый вечер"
    elif 0 <= hour < 6:
        message = "Доброй ночи"

    return message


def get_cards_and_expences_only(dict_) -> tuple[list[Any], DataFrame]:
    # собираем только те строки, в которых есть номера карт и сумма транзакции отрицательна,
    # что означает, что берем только платежи (расходы)
    cards = []
    expences_only = []
    for trans in dict_:
        try:
            if float(trans['Сумма операции']) < 0:
                cards.append(trans['Номер карты'][-5:])
                expences_only.append(trans)
        except Exception:
            continue

    # Собираем список из уникальных номеров карт
    cards = list(set(cards))

    # датафрейм только по платежам, очищенный от отсутствующих номеров карт
    expences = pd.DataFrame(expences_only)

    return cards, expences
