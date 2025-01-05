import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from pandas import Series

from src.utils import filter_by_dates

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
results_path = BASE_DIR + '\\results'

reports_logs_path = BASE_DIR + r'\logs\reports.log'

# настраиваем параметры логирования
reports_logger = logging.getLogger("reports")
file_handler = logging.FileHandler(reports_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)
reports_logger.setLevel(logging.INFO)


def spending_by_category(transactions: pd.DataFrame, months: int, category: str,
                         date_: str) -> Series:
    """
    Функция принимает данные транзакций, категорию и исходную дату.
    Возвращается датафрейм, содержащий траты по заданной категории
    за последние три месяца от переданной даты.
    """
    current_date = datetime.strptime(date_, '%d.%m.%Y %H:%M:%S')
    back_date = current_date - timedelta(days=months * 30)

    # фильтруем датасет по датам
    filtered_by_dates = filter_by_dates(transactions, back_date, current_date)
    df = pd.DataFrame(filtered_by_dates)

    # выбираем только заданные категории
    filtered_by_category = df.loc[df['Категория'] == category]

    # находим общую сумму платежей по этой категории
    expences_sum = filtered_by_category.agg({'Сумма операции': 'sum'})
    filtered_by_category.to_excel(results_path + r'\categories_3_months.xlsx')
    reports_logger.info("Запись файла categories_3_months.xlsx успешна.")

    return expences_sum
