import functools
import logging
from typing import Optional

import pandas as pd

from src.utils.utils_reports import sorted_by_month

loger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/reports.logs", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)



def save_report(filename):
    """
    Декоратор для записи возвращений функции в файл с форматом jsonl
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_json(filename, orient="records", lines=True, force_ascii=False)

            return result

        return wrapper

    return decorator

@save_report("data/reports.jsonl")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает Dataframe, категорию и дату(если не передается берет дату сегодня)
    возвращает Dataframe с колонами 'Категория', 'Дата платежа', 'Сумма операции с округлением'
    за 3 месяца от введенной даты
    """
    filtered_data = sorted_by_month(transactions, date)
    filtered_data = filtered_data[(filtered_data["Категория"] == category)]
    filtered_data["Дата платежа"] = pd.to_datetime(filtered_data["Дата платежа"], errors="coerce", dayfirst=True)
    filtered_data["Дата платежа"] = filtered_data["Дата платежа"].dt.strftime("%Y-%m-%d")
    return filtered_data[["Категория", "Дата платежа", "Сумма операции с округлением"]].reset_index(drop=True)


@save_report("data/reports.jsonl")
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] =  None) -> pd.DataFrame:
    """
    Функция принимает Dataframe и дату(если не передается берет дату сегодня), считает
    средние траты за день за 3 месяца от введеной даты,
    возвращает Dataframe с колонами  'Дата платежа', 'Средняя трата'
    """
    filtered_data = sorted_by_month(transactions, date)
    result = (
        filtered_data
        .groupby("Дата платежа", as_index=False)["Сумма операции с округлением"]
        .mean()
        .rename(columns={"Сумма операции с округлением": "Средняя трата"})
    )

    result["Средняя трата"] = result["Средняя трата"].round(2)

    return result.iloc[::-1].reset_index(drop=True)


