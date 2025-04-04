import pandas as pd
from unittest.mock import patch

import pytest

from src import reports


@pytest.mark.parametrize("category, expected", [
    ("food", 100),
    ("transport", 50),
])
def test_spending_by_category():
    mock_data = pd.DataFrame(
        {
            "Категория": ["Продукты", "Развлечения", "Продукты"],
            "Дата платежа": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-03-03"]),
        }
    )

    with patch("reports.sorted_by_month", return_value=mock_data):
        result = spending_by_category(mock_data, "Продукты", "2024-03-03")

        assert not result.empty
        assert all(result["Категория"] == "Продукты")
        assert "Дата платежа" in result.columns


def test_spending_by_weekday():
    mock_data = pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-03-03"]),
            "Сумма операции с округлением": [100, 200, 300],
        }
    )

    with patch("reports.sorted_by_month", return_value=mock_data):
        result = spending_by_weekday(mock_data, "2024-03-03")

        assert not result.empty
        assert "Средняя трата" in result.columns
        assert result["Средняя трата"].iloc[0] == 300


def test_save_report_decorator():
    mock_df = pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2024-03-01", "2024-03-02"]),
            "Сумма операции с округлением": [100.5, 200.75],
        }
    )

    with patch("pandas.DataFrame.to_json") as mock_to_json:
        spending_by_weekday(mock_df, "2024-03-03")

        mock_to_json.assert_called_once()
