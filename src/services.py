import datetime
import json
import logging
from typing import Any

logger = logging.getLogger("Logging")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/services.log", "w", "utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s", "%d.%m.%Y %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def investment_bank(month: str, transactions: list | Any, limit: int) -> str:
    """Рассчитывает сумму на счету инвесткопилки по заданному порогу округления"""
    logger.info("Старт")
    period = datetime.datetime.strptime(month, "%Y-%m")
    logger.info("Создание списка отфильтрованных транзакций")
    transactions_list = []
    investment_bank_sum = 0
    logger.info("Фильтрация транзакций по дате и занесение их суммы в список отфильтрованных транзакций")
    for transaction in transactions:
        transaction_date = transaction["operation_date"]
        payment_date = datetime.datetime.strptime(transaction_date, "%d.%m.%Y %H:%M:%S")
        if payment_date.month == period.month and transaction["payment_sum"] < 0:
            transactions_list.append(transaction["payment_sum"])
    logger.info("Расчет оставшейся суммы для инвестиционного банка")
    for transact in transactions_list:
        sum = abs(transact)
        diff = (sum // limit + 1) * limit - sum
        investment_bank_sum += diff
    logger.info("Создание json-файла с суммой для инвестиционного банка")
    result_list = []
    result_dict = {}
    result_dict["investment_bank"] = round(investment_bank_sum, 2)
    result_list.append(result_dict)
    result_list_jsons = json.dumps(result_list)
    logger.info("Стоп")
    return result_list_jsons
