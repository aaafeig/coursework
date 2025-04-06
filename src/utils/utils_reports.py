from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def sorted_by_month(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")

    end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_date = end_date - timedelta(days=90)
    transactions.loc[:, "Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], errors="coerce", dayfirst=True
    )

    filtered_data = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]

    return filtered_data
