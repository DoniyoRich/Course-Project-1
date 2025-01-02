import json
import logging
from json import JSONDecodeError
from pathlib import Path

from dotenv import load_dotenv
from datetime import datetime

from src.utils import greeting
from src.views import read_excel_and_filter_by_dates, every_card_details

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


def main():
    """ Основная функция программы, точка входа"""
    current_date_str = "30.12.2021 16:27:01"
    current_date = datetime.strptime(current_date_str, '%d.%m.%Y %H:%M:%S')
    start_date = current_date.replace(day=1, hour=0, minute=0, second=0)

    greeting_mes = greeting(current_date)

    try:
        with open(BASE_DIR + r'\user_settings.json') as u_sets:
            sets = json.load(u_sets)
            currencies = sets.get('user_currencies', 0)
            stocks = sets.get('user_stocks', 0)
            print(currencies, stocks)
            if currencies and stocks:
                print("Все ок")
                # convert_curr(currencies, 'RUB', stocks)
            else:
                print("Недостаточно данных для отображения")
                main_logger.warning("Недостаточно данных для отображения")

    except FileNotFoundError:
        print("Нет такого файла")
        main_logger.error("Нет такого файла")
    except JSONDecodeError:
        print("Ошибка чтения файла json")
        main_logger.error("Ошибка чтения файла json")

    filtered_by_dates = read_excel_and_filter_by_dates(transactions_path + r'\operations.xlsx', start_date, current_date)
    cards = every_card_details(filtered_by_dates)


# Запуск программы
if __name__ == '__main__':
    main()
