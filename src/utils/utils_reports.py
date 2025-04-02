from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def sorted_by_month(transactions: pd.DataFrame,  date: Optional[str] =  None) -> pd.DataFrame:
    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')

    end_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=90)
    transactions.loc[:, "Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], errors="coerce", dayfirst=True)


    filtered_data = transactions[
        (transactions["Дата платежа"] >= start_date) &
        (transactions["Дата платежа"] <= end_date)
        ]

    return filtered_data