import json
import re

import pandas as pd
from src.utils.utils_services import filtered_by_ym


def write_profitable_cashback_categories(data: str, year: str, month: str):
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

    sorted_services_cashback = dict(sorted(services_cashback.items(), key=lambda x: x[1], reverse=True))

    with open("data/services-cashback.json", "w", encoding="utf-8") as file:
        json.dump(sorted_services_cashback, file, ensure_ascii=False, indent=4)


def search_to_str(list_tran: list[dict], str_search: str) -> list[dict]:
    pattern = re.compile(str_search, re.IGNORECASE)
    operations =  [
        op for op in list_tran
        if pattern.search(str(op.get("Категория", ""))) or pattern.search(str(op.get("Описание", "")))
    ]
    return operations

def names_find(data: list[dict]):
    pattern = re.compile(r"\b[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.", re.IGNORECASE)

    operations = [
        op for op in data
        if op.get("Категория") == "Переводы" and pattern.search(str(op.get("Описание", "")))
    ]

    with open("data/services-names.json", "w", encoding="utf-8") as file:
        json.dump(operations, file, ensure_ascii=False, indent=4)
