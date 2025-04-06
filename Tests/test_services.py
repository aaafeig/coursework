import json
from unittest.mock import patch

import pytest

from src.services import (investment_bank, names_find, search_to_str,
                          tel_num_find, write_profitable_cashback_categories)


@pytest.fixture
def valid_data():
    return [{"category": "еда", "amount": 100}, {"category": "транспорт", "amount": 50}]

def test_search_to_str(valid_data):
    result = search_to_str(valid_data, "еда")
    assert isinstance(result, str), f"Функция должна возвращать строку, но получен {type(result)}"

def test_write_profitable_cashback_categories():
    data = [
        {"Категория": "Продукты", "Кэшбэк": 50},
        {"Категория": "Одежда", "Кэшбэк": 30},
        {"Категория": "Продукты", "Кэшбэк": 20},
        {"Категория": "Развлечения", "Кэшбэк": None},
    ]
    with patch("src.services.filtered_by_ym", return_value=data):
        result = write_profitable_cashback_categories("dummy_data", "2023", "05")
        expected = json.dumps(
            {"Продукты": 70, "Одежда": 30}, ensure_ascii=False, indent=4
        )
        assert result == expected


def test_investment_bank():
    transactions = [
        {"Дата операции": "2023-05", "Сумма операции": 245},
        {"Дата операции": "2023-05", "Сумма операции": 380},
        {"Дата операции": "2023-04", "Сумма операции": 150},
    ]
    result = investment_bank("2023-05", transactions, 100)
    assert result == (300 - 245) + (400 - 380)  # 55 + 20 = 75




def test_names_find():
    transactions = [
        {"Категория": "Переводы", "Описание": "Перевод Иванов И."},
        {"Категория": "Переводы", "Описание": "Перевод Петров П."},
        {"Категория": "Продукты", "Описание": "Покупка хлеба"},
    ]
    result = names_find(transactions)
    expected = json.dumps(transactions[:2], ensure_ascii=False, indent=4)
    assert result == expected


def test_tel_num_find():
    transactions = [
        {"Описание": "Звонок +7 999 123-45-67"},
        {"Описание": "Транзакция без телефона"},
        {"Описание": "Перевод на +7 495 678-90-12"},
    ]
    result = tel_num_find(transactions)
    expected = json.dumps(
        [transactions[0], transactions[2]], ensure_ascii=False, indent=4
    )
    assert result == expected
