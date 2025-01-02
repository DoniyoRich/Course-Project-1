import os

import requests
from black import datetime


def get_current_date() -> str:
    """
    Функция возвращает дату, введенную пользователем в строковом формате.
    Запрос от пользователя происходит до тех пор, пока не будет введена дата в требуемом формате.
    """
    correct_date = {
        'days': list(range(1, 32)),
        'months': list(range(1, 13)),
        'years': list(range(1900, 2025))
    }
    while True:
        try:
            date_curr = input("\nВведите текущую дату в формате дд.мм.гггг ЧЧ:ММ:СС : ").split(".")
            if int(date_curr[0]) in correct_date['days'] and int(date_curr[1]) in correct_date['months'] and (
                    int(date_curr[2])) in \
                    correct_date['years']:
                return '.'.join(date_curr)
            else:
                print('Что то не так с датой, попробуйте снова')
                continue
        except Exception:
            print("Неверный ввод, попробуйте снова")
            continue


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
