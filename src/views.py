import json
import logging
from typing import Any

from src.utils import (
    fetch_and_show_currency_rates,
    get_greeting,
    get_xlsx_data_dict,
    show_cards,
    show_top_5_transactions,
)

logger = logging.getLogger("Logging")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/views.log", "w", "utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s", "%d.%m.%Y %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_page(date: str) -> Any:
    """Записывает информацию для Главной страницы в файл json"""
    logger.info("Старт")
    logger.info("Преобразование файла Excel в список словарей")
    transactions = get_xlsx_data_dict("../data/operations.xlsx")
    logger.info("Получение приветствия")
    greeting = get_greeting(date)
    logger.info("Получение информации о карте")
    cards = show_cards(date, transactions)
    logger.info("Получение лучших сделок")
    top_transcations = show_top_5_transactions(date, transactions)
    logger.info("Получение валютных_курсов")
    currency_rates = fetch_and_show_currency_rates()
    logger.info("Создание словаря словарей")
    main_dict: dict = {}
    main_dict["greeting"] = greeting
    main_dict["cards"] = cards
    main_dict["top_transcations"] = top_transcations
    main_dict["currency_rates"] = currency_rates
    logger.info("Запись информации в json-файл")
    main_dict_jsons = json.dumps(main_dict, ensure_ascii=False, indent=4)
    with open("main.json", "w", encoding="utf-8") as f:
        json.dump(main_dict, f)
    logger.info("Стоп")
    return main_dict_jsons
