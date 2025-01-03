from typing import Any

import pandas as pd
# import requests
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

# def convert_curr(from_: list[str], to_: str) -> float:
#     """ Функция обращается к внешнему API и производит конвертацию валюты. """

# API_KEY_CURR = os.getenv("API_KEY_CURR")
# API_KEY_STOCK = os.getenv("API_KEY_STOCK")

#     response = []
#     for ind, currency in enumerate(from_):
#         response[ind] = requests.get(
#         f'https://api.apilayer.com/exchangerates_data/convert?to=]\
#         {to_}&from={from_[ind]}&amount={trans_amount}&apikey={API_KEY_CURR}')
#
#     if response.status_code == 200:
#         currency_rate = response.json()['info']['rate']
#         result = response.json()['result']
#         print(f"\nБыла произведена конвертация валюты из {from_} в {to_} по курсу: {currency_rate}")
#     else:
#         print("\nЧто-то пошло не так с запросом на конвертацию валюты.")
#         result = -1
#
#     return result
#
#
# url = "https://api.apilayer.com/exchangerates_data/convert"
#
# headers = {
#     "apikey": API_KEY
# }
#
# response = requests.get(url, headers=headers)
#
# user = "skypro-008"
# url = f"https://api.github.com/users/{user}/repos"
#
# response = requests.get(url)
#
# repos = response.json()
#
# for repo in repos:
#     if repo["language"] == "Python":
#         print(f"Name: {repo['name']}\nLink: {repo['html_url']}\n")
