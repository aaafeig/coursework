# import json
# import logging
# from datetime import datetime
#
# import pandas as pd
# import requests
#
# log = logging.getLogger(__name__)
# loger = logging.getLogger("log_views")
# file_handler = logging.FileHandler("logs/views.logs", mode="w", encoding="utf-8")
# file_formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
# )
# file_handler.setFormatter(file_formatter)
# loger.addHandler(file_handler)
# log.addHandler(file_handler)
# loger.setLevel(logging.DEBUG)
# log.setLevel(logging.DEBUG)
#
#
# # df = pd.read_excel("data/operations.xlsx")
# # operations = df.to_dict(orient="records")
#
#
# def get_date_range(date: str):
#     date_obj = datetime.strptime(date, "%d.%m.%Y")
#     start_of_month = date_obj.replace(day=1)
#     return start_of_month.strftime("%d.%m.%Y"), date_obj.strftime("%d.%m.%Y")
#
#
# def filtered_operations(time):
#     df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
#     start_date, end_date = get_date_range(time)
#     loger.info(f"Фильтруем с {start_date} по {end_date}")
#
#     loger.info(f"Минимальная дата в файле: {df['Дата операции'].min()}")
#     loger.info(f"Максимальная дата в файле: {df['Дата операции'].max()}")
#     df_filtered = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] < end_date)]
#     result = df_filtered.to_dict(orient="records")
#     log.info(f"Фильтрованные даты: {df_filtered['Дата операции'].tolist()}")
#
#     return result
#
# def greetings():
#     time_now = datetime.now
#     hours = time_now.hour
#     if 5 <= hours < 12:
#         greeting = "Доброе утро"
#     elif 12 <= hours < 18:
#         greeting = "Добрый день"
#     elif 18 <= hours < 22:
#         greeting = "Добрый вечер"
#     else:
#         greeting = "Доброй ночи"
#
#     return greeting



