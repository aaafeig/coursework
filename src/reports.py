import functools
import logging
from datetime import datetime, timedelta
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



def save_report(filename=None):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            report_filename = filename or f"{func.__name__}_report.txt"
            with open(report_filename, "w", encoding="utf-8") as file:
                file.write(str(result))

            return result

        return wrapper

    return decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    filtered_data = sorted_by_month(transactions, date)
    filtered_data = filtered_data[(filtered_data["Категория"] == category)]
    return filtered_data[["Категория", "Дата платежа"]].reset_index(drop=True)

def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] =  None) -> pd.DataFrame:
    filtered_data = sorted_by_month(transactions, date)
    result = (
        filtered_data
        .groupby("Дата платежа", as_index=False)["Сумма операции с округлением"]
        .mean()
        .rename(columns={"Сумма операции с округлением": "Средняя трата"})
    )

    result["Средняя трата"] = result["Средняя трата"].round(2)

    return result.iloc[::-1].reset_index(drop=True)


