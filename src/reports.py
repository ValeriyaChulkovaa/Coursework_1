import datetime
import json
import logging
from datetime import timedelta
from typing import Any, Callable

import pandas as pd

logger = logging.getLogger("Logging")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/reports.log", "w", "utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s", "%d.%m.%Y %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def decorator_spending_by_cat(func: Callable) -> Callable:
    """Логирует результат функции в файл по умолчанию spending_by_cat.json"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs).to_dict("records")
        with open("spending_by_cat.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result

    return wrapper


def log_spending_by_cat(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict("records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


def filtering_by_date(operations_df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Возвращает DataFrame за 3 месяца от указанной даты"""
    logger.info("Преобразование DF в словарь")
    operations = operations_df.to_dict("records")
    filtered_operations = []
    logger.info("Период создания в течение 90 дней")
    current_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    end_date = current_date - timedelta(days=90)
    logger.info("Фильтрация операций в течение 3 месяцев")
    for operation in operations:
        payment_date = datetime.datetime.strptime(str(operation["Дата операции"]), "%d.%m.%Y %H:%M:%S")
        if end_date < payment_date < current_date:
            filtered_operations.append(operation)
    logger.info("Преобразование данных обратно в DF")
    filtered_operations_df = pd.DataFrame(filtered_operations)
    logger.info("Возврат DF к основной функции")
    return filtered_operations_df


@decorator_spending_by_cat
def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> pd.DataFrame:
    """Возвращает DataFrame по заданной категории за 3 месяца от указанной даты"""
    logger.info("Старт")
    logger.info("Создание отфильтрованного списка по дате за последние 3 месяца с помощью другой функции")
    transactions_filtered_by_3_months = filtering_by_date(transactions, date)
    logger.info("Фильтрация транзакций по категориям")
    if transactions_filtered_by_3_months.empty:
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если нет транзакций
    category_transcations = transactions_filtered_by_3_months[
        transactions_filtered_by_3_months["Категория"] == category
    ]
    logger.info("Возвращение отфильтрованного DF")
    logger.info("Стоп")
    return category_transcations
