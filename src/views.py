import json
from collections import defaultdict

import pandas as pd

from src.utils.utils_views import (count_amount, currency_rates,
                                   filtered_operations, find_period_of_time,
                                   greetings, info_about_operations, top5_tran,
                                   transfers_and_cash)


def write_json_gl(time_setting: str):
    """
    Функция возращает json, отфильтрованные транзакции от введеной даты до начала месяца
    с информацией о картах (траты, кэшбек), топ 5 транзакций и курс валют и акций
    """
    operations = filtered_operations(time_setting)
    greet = greetings()
    card_numbers, amounts, cashback = info_about_operations(operations)
    top_transactions = top5_tran(operations)
    currency_data, stock_data = currency_rates("data/user_settings.json")

    card_data = defaultdict(lambda: {"total_spent": 0, "cashback": 0})

    for card, amount, cash in zip(card_numbers, amounts, cashback):
        last_digits = card[-4:] if pd.notna(card) and len(str(card)) >= 4 else "----"
        card_data[last_digits]["total_spent"] += amount if pd.notna(amount) else 0
        card_data[last_digits]["cashback"] += cash if pd.notna(cash) else 0

    cards_info = [
        {
            "last_digits": card,
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(data["cashback"], 2),
        }
        for card, data in card_data.items()
    ]

    top_transactions_info = [
        {
            "date": op.get("Дата платежа", ""),
            "amount": op.get("Сумма операции с округлением", 0),
            "category": op.get("Категория", ""),
            "description": op.get("Описание", ""),
        }
        for op in top_transactions
    ]

    information_json = {
        "greeting": greet,
        "cards": cards_info,
        "top_transactions": top_transactions_info,
        "currency_rates": currency_data,
        "stock_prices": stock_data,
    }

    return json.dumps(information_json, ensure_ascii=False, indent=4)


def write_json_sob(date: str, period_of_time: str = "W"):
    """
    Функция фильтрует транзакции по дате и второму параметру, который определяет диапозон
    (неделя, месяу, год, все траназацкии до даты и возращает json с информацией о расходах, поступлениях
    и курс валют с акций)
    """

    operations = find_period_of_time(date, period_of_time)
    currency_data, stock_data = currency_rates("data/user_settings.json")

    tr_and_ch = transfers_and_cash(operations)
    total_amount_ex, transactions_for_circle, total_amount_ic, transactions_income = (
        count_amount(operations)
    )

    information_json = {
        "expenses": {
            "total_amount": round(total_amount_ex, 2),
            "main": transactions_for_circle,
            "transfers_and_cash": tr_and_ch,
        },
        "income": {"total_amount": total_amount_ic, "main": transactions_income},
        "currency_rates": currency_data,
        "stock_prices": stock_data,
    }

    return json.dumps(information_json, ensure_ascii=False, indent=4)
