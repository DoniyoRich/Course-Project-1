import json
import logging
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

from dotenv import load_dotenv

from src.utils import greeting
from src.views import (cards_total_spent, get_currency_rates, get_stock_prices, get_top_transactions,
                       read_excel_and_filter_by_dates)

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
transactions_path = BASE_DIR + '\\data'

main_logs_path = BASE_DIR + r'\logs\main.log'

main_logger = logging.getLogger("main")
file_handler = logging.FileHandler(main_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
main_logger.addHandler(file_handler)
main_logger.setLevel(logging.INFO)

# загружаем ключи
load_dotenv(BASE_DIR + '\\.env')


def main(date_curr: str) -> str:
    """ Функция получает текущую дату и возвращает json ответ для главной страницы сайта"""

    current_date = datetime.strptime(date_curr, '%d.%m.%Y %H:%M:%S')
    start_date = current_date.replace(day=1, hour=0, minute=0, second=0)
    print(f"\nНачало отчетного периода: {start_date}")
    print(f"Конец отчетного периода: {current_date}")

    # формируем приветствие в зависимости от времени суток
    # берется от текущей даты и времени, предоставленной пользователем
    greeting_message = greeting(current_date)

    # читаем файл с транзакциями
    # и формируем датасет, состоящий из транзакций (только платежи) согласно заданного диапазона
    # и очищенный от записей с отсутствующими номерами карт
    filtered_by_dates = read_excel_and_filter_by_dates(transactions_path + r'\operations.xlsx', start_date,
                                                       current_date)
    # получаем список словарей, где ключами являются номер карты, общая сумма расходов, кэшбэк
    cards_total_expences = cards_total_spent(filtered_by_dates)

    top_transactions = get_top_transactions(filtered_by_dates)

    # получаем список валют и акций из json файла
    # для начала инициализируем их пустыми списками,
    # если возникнет проблема с файлом-источником данных
    currencies = []
    stocks = []

    try:
        with open(BASE_DIR + r'\user_settings.json') as u_sets:
            sets = json.load(u_sets)
            currencies = sets.get('user_currencies', 0)
            stocks = sets.get('user_stocks', 0)

    except FileNotFoundError:
        print("Нет такого файла")
        main_logger.error("Нет такого файла")
    except JSONDecodeError:
        print("Ошибка чтения файла json")
        main_logger.error("Ошибка чтения файла json")

    currency_rates = get_currency_rates(currencies) # функция рабочая, просто временно отключена, чтобы экономить запросы
    stock_prices = get_stock_prices(stocks)  # функция рабочая, просто временно отключена, чтобы экономить запросы
    # stock_prices = []     # временная заглушка, потом нужно ее удалить и раскомментировать верхнюю строчку
    # currency_rates = []     # временная заглушка, потом нужно ее удалить и раскомментировать верхнюю строчку

    # Формируем словарь перед конвертацией в json согласно формату, представленному в тз
    main_page = {
        "greeting": greeting_message,
        "cards": cards_total_expences,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    # конвертируем готовый ответ в json
    main_page_json = json.dumps(main_page, ensure_ascii=False, indent=4)
    print('\nJSON ответ для главной страницы:')

    return main_page_json


# Запуск программы, точка входа
if __name__ == '__main__':
    # Фиксируем определенную дату для передачи в функцию
    current_date_str = "30.12.2021 19:27:01"

    # Готовый json ответ для главной страницы сайта
    json_main_page = main(current_date_str)
    print(json_main_page)

    with open(BASE_DIR + r'\logs\main_page.json', 'w', encoding='UTF-8') as file_json:
        file_json.write(json_main_page)
        main_logger.info("файл main_page.json создан успешно")
