import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.utils import get_cards_and_expences_only

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
views_logs_path = BASE_DIR + r'\logs\views.log'

# настраиваем параметры логгирования
views_logger = logging.getLogger("views")
file_handler = logging.FileHandler(views_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.setLevel(logging.INFO)


def read_excel_and_filter_by_dates(file_path, start_date: datetime, current_date: datetime) -> list[dict]:
    """ Функция принимает пусть к файлу формата excel и возвращает список словарей. """
    try:
        print("\nЧитаю excel файл с транзакциями, может занять некоторое время...")

        # пытаемся открыть и сохранить датафрейм из эксель файла
        transactions = pd.read_excel(file_path).to_dict(orient="records")

        views_logger.info(f"Успешное чтение файла {file_path}")

        # В этом списке будем собирать транзакции в заданном диапазоне дат
        filtered_by_dates = []
        for transaction in transactions:
            transaction['date_formatted'] = \
                datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S')
            if transaction['Статус'] == 'OK':
                if start_date <= transaction['date_formatted'] <= current_date:
                    filtered_by_dates.append(transaction)

        # df = pd.DataFrame(filtered_by_dates)
        # df.to_excel('test_excel_writing.xlsx')
        return filtered_by_dates

    except FileNotFoundError:
        views_logger.error(f"Ошибка чтения файла {file_path}")
        return []


def cards_total_spent(dict_: dict) -> list:
    """
    Функция получает отфильтрованный словарь по датам
    и возвращает список из словарей для всех карт, общую сумму расходов по каждой карте
    за заданный период, а также сумму кэшбека
    """

    # переводим словарь в датафрейм для удобства преобразований
    cards, expences_only = get_cards_and_expences_only(dict_)
    expences = pd.DataFrame(expences_only)
    # expences.to_excel('test_excel_writing_negatives.xlsx')

    # собираем список транзакций, группированные по каждой карте
    cards_df = []
    for card_ in cards:
        cards_df.append(expences.loc[expences["Номер карты"] == card_])

    # собираем общую сумму расходов по каждой карте
    total_expences = []
    for card in cards_df:
        total_expences.append(card.agg({'Сумма операции': 'sum'}).to_dict())

    # формируем список словарей, где ключами являются номер карты, общая сумма расходов, кэшбэк
    cards_expences = []
    for card_number, expence in zip(cards, total_expences):
        # print(card_number, round(abs(expence['Сумма операции']), 2), round(abs(expence['Сумма операции']) / 10), 2)
        exp_sum = round(abs(expence['Сумма операции']), 2)
        cashback = round(abs(expence['Сумма операции']) / 100, 2)
        cards_expences.append({'last_digits': card_number[-4:], 'total_spent': exp_sum,
                               'cashback': cashback})

    # Временный тестовый блок для проверки правильности работы функции.
    # Выводит результат работы функции в отдельный json файл в папке logs текущего проекта
    with open(BASE_DIR + r'\logs\test_json.json', 'w') as test_file:
        json.dump(cards_expences, test_file)
        views_logger.info("файл test_json.json создан успешно")

    return cards_expences
