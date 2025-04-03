import json
import logging
import math
import re

import pandas as pd

from src.utils.utils_services import filtered_by_ym

loger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/services.logs", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)


def write_profitable_cashback_categories(data: str, year: str, month: str):
    """
    Функция возращает json о выгодных кэшбеках
    """
    operations = filtered_by_ym(data, year, month)
    services_cashback = {}
    for ops in operations:
        category = ops["Категория"]
        cashback = ops.get("Кэшбэк", 0)
        if pd.notna(cashback) and cashback > 0 and pd.notna(category):
            if category in services_cashback:
                services_cashback[category] += cashback
            else:
                services_cashback[category] = cashback

    sorted_services_cashback = dict(
        sorted(services_cashback.items(), key=lambda x: x[1], reverse=True)
    )

    return json.dumps(sorted_services_cashback, ensure_ascii=False, indent=4)


def investment_bank(
    month: str, transactions: list[dict[str, any]], limit: int
) -> float:
    """
    Функция округляет сумму до лимита и возвращает разницу между суммой и округленной суммой
    """
    total_savings = 0

    filtered_trans = [op for op in transactions if op["Дата операции"] == month]
    for transaction in filtered_trans:
        amount = transaction.get("Сумма операции", 0)
        rounded_amount = math.ceil(amount / limit) * limit
        savings = rounded_amount - amount
        total_savings += savings
    loger.debug(
        f"Проверка проходила по критериям: {transactions[0]['Дата операции']} равно {month}"
    )

    return round(total_savings, 2)


def search_to_str(list_tran: list[dict], str_search: str):
    """
    Функция для поиска всех транзакций с введенной категорией
    """
    pattern = re.compile(str_search, re.IGNORECASE)
    operations = [
        op
        for op in list_tran
        if pattern.search(str(op.get("Категория", "")))
        or pattern.search(str(op.get("Описание", "")))
    ]
    return operations


def names_find(data: list[dict]):
    """
    Функция для поиска всех транзакций с введенным именем
    """
    pattern = re.compile(r"\b[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.", re.IGNORECASE)

    operations = [
        op
        for op in data
        if op.get("Категория") == "Переводы"
        and pattern.search(str(op.get("Описание", "")))
    ]

    return json.dumps(operations, ensure_ascii=False, indent=4)


def tel_num_find(data):
    """
    Функция для поиска всех транзакциях с введеным номером телефона
    """
    pattern = re.compile(r"\+7\s\d{3}\s\d{2,3}-\d{2}-\d{2}")

    phone_operation = [op for op in data if pattern.search(str(op.get("Описание", "")))]

    return json.dumps(phone_operation, ensure_ascii=False, indent=4)
