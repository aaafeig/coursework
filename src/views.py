import json
from datetime import datetime

import pandas as pd
import requests


df = pd.read_excel("data/operations.xlsx")
operations = df.to_dict(orient="records")


def write_in_json():
    hello = greetings()
    card_info = cards("2200 - 4311 - 6332 - 4113", 8000)
    list_cards = [card_info]
    json_info = {"greetings": hello, "cards": list_cards}
    with open("data/information.json", "w") as file:
        json.dump(json_info, file)


def get_date_range(date: str):
    date_obj = datetime.strptime(date, "%d.%m.%Y")
    start_of_month = date_obj.replace(day=1)
    return start_of_month.strftime("%d.%m.%Y"), date_obj.strftime("%d.%m.%Y")


def greetings():
    time_now = datetime.now()
    hour = time_now.hour
    if 5 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Good day"
    elif 18 <= hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    return greeting


def cards(card_number, total_expenses):
    last_digits = card_number[-4:]
    cashback = total_expenses / 100
    cards_information = {
        "last_digits": last_digits,
        "total_spent": total_expenses,
        "cashback": cashback,
    }
    return cards_information

def top_transactions():
    date = datetime.today()
