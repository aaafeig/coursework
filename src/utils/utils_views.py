import json
import logging
import os
from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

loger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/views.logs", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)

load_dotenv()
API_KEY_CUR_USD = os.getenv("API_KEY_CUR_USD")
API_KEY_POS = os.getenv("API_KEY_STOCK")


df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def get_date_range(date: str) -> tuple[str, str]:
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_month = date_obj.replace(day=1)
    return start_of_month.strftime("%d.%m.%Y"), date_obj.strftime("%d.%m.%Y")


def filtered_operations(time: str) -> list[dict]:
    start_date, end_date = get_date_range(time)
    start_date = pd.to_datetime(start_date, dayfirst=True)
    end_date = pd.to_datetime(end_date, dayfirst=True)
    loger.debug(f"Сортировки от {start_date} до {end_date}")
    filtered_op = [
        op
        for op in operations_df
        if start_date <= pd.to_datetime(op["Дата операции"], dayfirst=True) <= end_date
    ]
    return filtered_op


def greetings() -> str:
    time_now = datetime.now().hour
    if 5 <= time_now < 12:
        greeting = "Доброе утро"
    elif 12 <= time_now < 18:
        greeting = "Добрый день"
    elif 18 <= time_now < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    return greeting


def info_about_operations(operations: list[dict]) -> tuple[list, list, list]:
    information_cards = []
    information_amount = []
    information_cashback = []

    for op in operations:
        card_number = op.get("Номер карты", "Неизвестно")
        amount = op.get("Сумма операции с округлением", 0)
        cashback = op.get("Кэшбэк", 0)

        information_cards.append(card_number)
        information_amount.append(amount)
        information_cashback.append(cashback)

    return (
        information_cards,
        information_amount,
        information_cashback,
    )


def top5_tran(operations: list[dict]) -> list[dict]:
    top_transactions = sorted(
        operations, key=lambda x: x["Сумма операции с округлением"], reverse=True
    )
    return top_transactions[:5]


def currency_rates(user_settings: str) -> tuple[list, list]:
    currency_info = []
    stocks_info = []
    with open(user_settings, encoding="utf-8") as file:
        settings = json.load(file)

    currencies = ",".join(settings["user_currencies"])
    url_currency = f"http://api.currencylayer.com/live?access_key={API_KEY_CUR_USD}&currencies={currencies}"

    response_currency = requests.get(url_currency)
    data_currency = response_currency.json()
    loger.debug(data_currency)
    if "quotes" in data_currency:
        for currency in settings["user_currencies"]:
            key = f"{currency}RUB"  # USDRUB
            if key in data_currency["quotes"]:
                currency_info.append(
                    {
                        "currency": currency,
                        "rate": round(data_currency["quotes"][key], 2),
                    }
                )
            loger.debug("Все сработало")
        else:
            loger.debug("Ошибка при получении данных или неверный API-ключ.")

    stocks = ",".join(settings["user_stocks"])
    url_stocks = f"http://api.marketstack.com/v1/eod/latest?access_key={API_KEY_POS}&symbols={stocks}"
    response_stocks = requests.get(url_stocks)
    data_stocks = response_stocks.json()
    loger.debug(data_stocks)

    if "data" in data_stocks:
        for stock in data_stocks["data"]:
            stocks_info.append(
                {"stock": stock["symbol"], "price": float(stock["close"])}
            )

    return currency_info, stocks_info


def find_period_of_time(date: str, setting_time: str = "W") -> list[dict]:
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    if setting_time == "W":
        start = date_obj - timedelta(days=date_obj.weekday())
        end = start + timedelta(days=6)

    elif setting_time == "M":
        start = date_obj.replace(day=1)
        next_month = date_obj.month % 12 + 1
        next_year = date_obj.year + (date_obj.month // 12)
        end = datetime(next_year, next_month, 1) - timedelta(days=1)

    elif setting_time == "Y":
        start = datetime(date_obj.year, 1, 1)
        end = datetime(date_obj.year, 12, 31)

    elif setting_time == "ALL":
        start = datetime(1900, 1, 1)
        end = date_obj
    else:
        raise ValueError("Неверный диапазон. Используйте 'W', 'M', 'Y' или 'ALL'.")

    loger.debug(f"Даты остсортироавлись от {start} и {end}")

    interval_time = [
        op
        for op in operations_df
        if start <= pd.to_datetime(op["Дата операции"], dayfirst=True) <= end
    ]

    return interval_time


def transfers_and_cash(operations: list[dict]) -> list[dict]:
    tr_and_cash = [
        {
            "category": op.get("Категория", ""),
            "amount": op.get("Сумма операции с округлением", 0),
        }
        for op in operations
        if op.get("Категория", "").lower() in ["наличные", "переводы"]
    ]
    return sorted(tr_and_cash, key=lambda x: x["amount"], reverse=True)


def count_amount(operations: list[dict]) -> tuple[float, list, float, list]:
    expenses = defaultdict(float)
    income = defaultdict(float)

    for op in operations:
        category = op.get("Категория", "").strip()
        amount = op.get("Сумма операции с округлением", 0)

        if category.lower() in ["пополнения", "проценты", "бонусы"]:
            income[category] += amount
        else:
            expenses[category] += amount

    total_amount_ex = sum(expenses.values())
    total_amount_ic = sum(income.values())

    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    top_expenses = sorted_expenses[:7]
    other_expense_amount = sum(amount for _, amount in sorted_expenses[7:])

    transactions_for_circle = [
        {"category": cat, "amount": round(amt, 2)} for cat, amt in top_expenses
    ]

    if other_expense_amount > 0:
        transactions_for_circle.append(
            {"category": "Остальное", "amount": other_expense_amount}
        )

    sorted_income = sorted(income.items(), key=lambda x: x[1], reverse=True)
    transactions_income = [
        {"category": cat, "amount": amt} for cat, amt in sorted_income
    ]

    return (
        total_amount_ex,
        transactions_for_circle,
        total_amount_ic,
        transactions_income,
    )
