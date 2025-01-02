import logging
from pathlib import Path

import pandas as pd
from win32ctypes.pywin32.pywintypes import datetime

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

        print(f'Количество записей в заданном диапазоне: {len(filtered_by_dates)}')

        # df = pd.DataFrame(filtered_by_dates)
        # df.to_excel('test_excel_writing.xlsx')
        return filtered_by_dates

    except FileNotFoundError:
        views_logger.error(f"Ошибка чтения файла {file_path}")
        return []


def every_card_details(dict_: dict) -> list:
    """
    Функция получает отфильтрованный словарь по датам
    и возвращает список из словарей для всех карт, общую сумму расходов по каждой карте
    за заданный период, а также сумму кэшбека
    """
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
    print(cards)

    # переводим словарь в датафрейм для удобства преобразований
    expences_only = pd.DataFrame(expences_only)
    expences_only.to_excel('test_excel_writing_negatives.xlsx')

    # собираем список транзакций, группированные по каждой карте
    cards_df = []
    for card in cards:
        cards_df.append(expences_only.loc[expences_only['Номер карты'] == card])

    print(cards_df)

    expences_and_cashback = []
    for card in cards_df:
        expences_and_cashback.append(card.agg({'Сумма операции': 'sum'}).to_dict())

    print(expences_and_cashback)
    # for index, row in not_null_trans.iterrows():
    #     italy_reviews = reviews.loc[reviews.country == 'Italy']
    #     print(row['Категория'])
    # input()

    # for ind, card in enumerate(cards):
    #     print(transactions['Номер карты'])
    #     print(ind, card)
    #     print(transactions.loc[transactions['Номер карты']] == card)

    #     cards_df.append(transactions.loc[transactions['Номер карты']] == card)
    # print(cards_df)
