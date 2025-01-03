import json
import logging
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

from dotenv import load_dotenv

from src.utils import greeting
from src.views import cards_total_spent, read_excel_and_filter_by_dates

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
    current_date_str = "15.12.2021 16:27:01"
    current_date = datetime.strptime(current_date_str, '%d.%m.%Y %H:%M:%S')
    start_date = current_date.replace(day=1, hour=0, minute=0, second=0)

    # формируем приветствие в зависимости от времени суток
    # берется от текущей даты и времени, предоставленной пользователем
    greeting_message = greeting(current_date)
    print(greeting_message)

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

    # читаем файл с транзакциями
    # и формируем датасет, состоящий из транзакций (только платежи) согласно заданного диапазона
    # и очищенный от записей с отсутствующими номерами карт
    filtered_by_dates = read_excel_and_filter_by_dates(transactions_path + r'\operations.xlsx', start_date,
                                                       current_date)

    # получаем список словарей, где ключами являются номер карты, общая сумма расходов, кэшбэк
    cards_total_expences = cards_total_spent(filtered_by_dates)
    print(cards_total_expences)


# Запуск программы
if __name__ == '__main__':
    main()
