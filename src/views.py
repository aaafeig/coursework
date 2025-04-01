from src.utils.utils_views import *


def write_in_json_gl(time_setting):
    operations = filtered_operations(time_setting)
    greet = greetings()
    card_numbers, amounts, cashbacks = info_about_operations(operations)
    top_transactions = top5_tran(operations)
    currency_data, stock_data = currency_rates("data/user_settings.json")

    cards_info = []
    for card, amount, cashback in zip(card_numbers, amounts, cashbacks):
        last_digits = (
            str(card)[-4:] if pd.notna(card) and len(str(card)) >= 4 else "----"
        )
        cashback = cashback if pd.notna(cashback) else 0
        cards_info.append(
            {"last_digits": last_digits, "total_spent": amount, "cashback": cashback}
        )

    top_transactions_info = []
    for op in top_transactions:
        top_transactions_info.append(
            {
                "date": op.get("Дата платежа", ""),
                "amount": op.get("Сумма операции с округлением", 0),
                "category": op.get("Категория", ""),
                "description": op.get("Описание", ""),
            }
        )

    information_json = {
        "greeting": greet,
        "cards": cards_info,
        "top_transactions": top_transactions_info,
        "currency_rates": currency_data,
        "stock_prices": stock_data,
    }

    with open("data/information-Glavnaya.json", "w", encoding="utf-8") as file:
        json.dump(information_json, file, ensure_ascii=False, indent=4)


def write_in_json_sob(date: str, period_of_time: str = "W"):
    operations = find_period_of_time(date, period_of_time)
    currency_data, stock_data = currency_rates("data/user_settings.json")

    tr_and_ch = transfers_and_cash(operations)
    total_amount_ex, transactions_for_circle, total_amount_ic, transactions_income = (
        count_amount(operations)
    )

    information_json = {
        "expenses": {
            "total_amount": total_amount_ex,
            "main": transactions_for_circle,
            "transfers_and_cash": tr_and_ch,
        },
        "income": {"total_amount": total_amount_ic, "main": transactions_income},
        "currency_rates": currency_data,
        "stock_prices": stock_data,
    }

    with open("data/information-Sobitia.json", "w", encoding="utf-8") as file:
        json.dump(information_json, file, ensure_ascii=False, indent=4)