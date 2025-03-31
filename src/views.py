import json
import logging
import math
from datetime import datetime

import pandas as pd
import requests

log = logging.getLogger(__name__)
loger = logging.getLogger("log_views")
file_handler = logging.FileHandler("logs/views.logs", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
log.addHandler(file_handler)
loger.setLevel(logging.DEBUG)
log.setLevel(logging.DEBUG)


df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def write_in_json(time):
    operations = filtered_operations(time)
    greet = greetings()
    card_numbers, amounts, cashbacks = info_about_operations(operations)
    top_transactions = top5_tran(operations)

    cards_info = []
    for card, amount, cashback in zip(card_numbers, amounts, cashbacks):
        cards_info.append({
            "last_digits": str(card)[-4:],  # Последние 4 цифры карты
            "total_spent": amount,
            "cashback": cashback
        })

    top_transactions_info = []
    for op in top_transactions:
        top_transactions_info.append({
            "date": op.get("Дата платежа", ""),
            "amount": op.get("Сумма операции с округлением", 0),
            "category": op.get("Категория", ""),
            "description": op.get("Описание", "")
        })

    information_json = {
        "greeting": greet,
        "cards": cards_info,
        "top_transactions": top_transactions_info
    }

    with open("data/information.json", 'w', encoding='utf-8') as file:
        json.dump(information_json, file, ensure_ascii=False, indent=4)

    print("Данные успешно записаны в information.json")



def get_date_range(date: str) -> tuple[str, str]:
    date_obj = datetime.strptime(date, "%d.%m.%Y")
    start_of_month = date_obj.replace(day=1)
    return start_of_month.strftime("%d.%m.%Y"), date_obj.strftime("%d.%m.%Y")


def filtered_operations(time):
    start_date, end_date = get_date_range(time)
    start_date =  pd.to_datetime(start_date, dayfirst=True)
    end_date =  pd.to_datetime(end_date, dayfirst=True)
    filtered_op = [op for op in operations_df if start_date <= pd.to_datetime(op['Дата платежа'], dayfirst=True) <= end_date]
    return filtered_op


def greetings():
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


def info_about_operations(operations) -> tuple[list, list, list]:
    information_cards = []
    information_amount = []
    information_cashback = []

    for op in operations:
        card_number = op.get('Номер карты', 'Неизвестно')
        amount = op.get('Сумма операции с округлением', 0)
        cashback = op.get('Кэшбэк', 0)

        information_cards.append(card_number)
        information_amount.append(amount)
        information_cashback.append(cashback)

    return information_cards, information_amount,information_cashback,

def top5_tran(operations):
    top_transactions = sorted(operations, key=lambda x: x["Сумма операции с округлением"], reverse=True)
    return top_transactions[:5]


def currency_rates(operations):
    with open('date/user_settings.json', encoding="utf-8") as file_json:
        currency = json.load(file_json)