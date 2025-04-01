import logging

import pandas as pd

loger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/views.logs", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)




def filtered_by_ym(data: str, year: str, month: str) -> list[dict]:
    year = int(year)
    month = int(month)

    df = pd.read_excel(data)

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True, errors='coerce')
    df = df.dropna(subset=["Дата платежа"])

    filtered_df = df[(df["Дата платежа"].dt.year == year) & (df["Дата платежа"].dt.month == month)]

    return filtered_df.to_dict(orient="records")

