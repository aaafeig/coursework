from src.reports import spending_by_category, spending_by_weekday
from src.services import write_profitable_cashback_categories, investment_bank, search_to_str, names_find, tel_num_find
from src.views import write_json_gl, write_json_sob
import pandas as pd

df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def main():
    print(f'''Категория "Веб-старницы":
    {write_json_gl("2018-05-18 00:00:00")}
    {write_json_sob("2018-05-18 00:00:00")}
    Категория "Сервисы":
    {write_profitable_cashback_categories("data/operations.xlsx", "2018", "05")}
    {investment_bank("2018-05", operations_df, 50)}
    {search_to_str(operations_df, "Рестораны")}
    {names_find(operations_df)}
    {tel_num_find(operations_df)}
    Категория "Отчеты":
    {spending_by_category(df, "Рестораны", "2018-05-18 00:00:00")}
    {spending_by_weekday(df, "2018-05-18 00:00:00")}''')


if __name__ == "__main__":
    main()
