from src.settings_logger import setup_logger

import pandas as pd
import requests

from src.utils import PATH, load_operations, get_user_settings, get_month_range
from dotenv import load_dotenv
import os
import json
from datetime import datetime

PERCENT_CASHBACK = 0.01

logger = setup_logger(__name__,"DEBUG", "views.log")

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_FOR_STOCKS = os.getenv("API_KEY_FOR_STOCKS")

if not API_KEY or not API_KEY_FOR_STOCKS:
    raise RuntimeError("API keys are not set in environment variables")


def get_greeting(date: str) -> str:
    """
    Функция возвращает «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего
    времени.
    :param date: Дата.
    :return: Строка с приветствием.
    """
    logger.info("Convert a date from type 'str' to a datetime object.")
    try:
        date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    except (TypeError, ValueError):
        logger.exception(f"Error converting date: %s", date)

    if 6 <= date.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= date.hour < 18:
        greeting = "Добрый день"
    elif 18 <= date.hour < 24:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    logger.info("Returns the user's greeting depending on the time of day.")
    return  greeting


def get_cards_expenses_and_cashback(transactions: pd.DataFrame) -> list[dict]:
    """
    Функция возвращает список словарей, которые содержат информацию о последних 4 цифры карты, общая сумма расходов,
    кешбэк (1 рубль на каждые 100 рублей).
    :param transactions: Dataframe, который содержит данные о транзакциях.
    :return: Список словарей с необходимыми данными.
    """
    logger.info("Starting calculation of expenses and cashback by card.")
    expenses = transactions[transactions['Сумма платежа'] < 0]
    logger.debug("Filtered expenses count: %d", len(expenses))

    grouped = expenses.groupby("Номер карты")['Сумма платежа'].sum().abs().round(2).reset_index()
    grouped.rename(columns={"Сумма платежа": "total_spent"}, inplace=True)

    grouped["last_digits"] = grouped["Номер карты"].str.replace("*", "", regex=False)
    grouped["cashback"] = (grouped["total_spent"] * PERCENT_CASHBACK).round(2)

    result = grouped.loc[:, ["last_digits", "total_spent", "cashback"]]
    logger.info("Calculated expenses and cashback for %d cards.", len(result))
    return result.to_dict(orient="records")


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """
    Функция возвращает топ-5 транзакций по сумме платежа.
    :param transactions: Dataframe с транзакциями.
    :return: Список топ-5 транзакций по сумме платежа.
    """
    logger.info("Start processing top 5 transactions.")
    expenses = transactions[transactions['Сумма платежа'] < 0].copy()
    logger.debug("Filtered expenses count: %d", len(expenses))

    top_5 = expenses.sort_values(by='Сумма платежа', key=lambda x: x.abs(), ascending=False).head(5)

    top_5 = top_5[["Дата операции", "Сумма платежа", "Категория", "Описание"]].copy()
    top_5.rename(columns={
        "Дата операции": "date",
        "Сумма платежа": "amount",
        "Категория": "category",
        "Описание": "description"
    }, inplace=True)

    top_5["date"] = top_5["date"].dt.strftime("%d.%m.%Y")
    top_5["amount"] = top_5["amount"].abs().round(2)

    logger.info("Completed formatting top transactions.")
    return top_5.to_dict(orient="records")


def get_currency_rates(currencies: list) -> list[dict]:
    """
    Функция возвращает ставку курса валют относительно валюты - RUB.
    :return: Список с валютами и их ставками.
    """
    base_currency = "RUB"

    url =  "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": API_KEY}
    params = {"symbols": ",".join(currencies), "base": base_currency}

    logger.info("Requesting currency rates for: %s", currencies)
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info("Currency rates successfully retrieved.")
    except requests.exceptions.RequestException as req_err:
        logger.error("[HTTP Error]: %s", req_err)
        raise
    except json.JSONDecodeError as json_err:
        logger.error("[JSON Decode Error]: %s", json_err)
        raise

    if "rates" not in data:
        logger.error("API response missing 'rates' field")
        raise ValueError("API response missing 'rates' field")

    result = []
    for currency, rate in data["rates"].items():
        invert_rate = round(1 / rate, 2)
        result.append({"currency": currency, "rate": invert_rate})

    logger.debug("Parsed currency rates: %s", result)
    return result


def get_stock_prices(stocks: list) -> list[dict]:
    """
    Функция возвращает стоимость акций из S&P500.
    :param stocks: Список акций.
    :return: Список со стоимостью акций.
    """
    url = "https://api.stockdata.org/v1/data/quote"
    stocks =  [stocks[:2], stocks[2:]]
    result = []

    logger.info("Requesting stock prices for: %s", stocks)
    for stock in stocks:
        params = {"symbols": ",".join(stock), "api_token": API_KEY_FOR_STOCKS}
        try:
            logger.info("Fetching data for stock group: %s", stock)
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as req_err:
            logger.error("[HTTP Error]: %s", req_err)
            raise
        except json.JSONDecodeError as json_err:
            logger.error("[JSON Decode Error]: %s", json_err)
            raise

        logger.info("Stock prices successfully retrieved.")
        for stock_info in data.get("data"):
            result.append({"stock": stock_info.get("ticker"), "price": stock_info.get("price")})

    logger.info("Parsed stock prices: %s", result)
    return result


def home_page(date: str) -> str:
    """
    Основная функция для формирования домашней страницы пользователя в формате JSON.

    Принимает строку с датой и временем (в формате 'YYYY-MM-DD HH:MM:SS'),
    и возвращает JSON-ответ, содержащий следующую информацию:

    1. Персонализированное приветствие в зависимости от времени суток:
       - "Доброе утро" (с 06:00 до 11:59)
       - "Добрый день" (с 12:00 до 17:59)
       - "Добрый вечер" (с 18:00 до 23:59)
       - "Доброй ночи" (с 00:00 до 05:59)

    2. Информация по каждой карте:
       - последние 4 цифры номера карты;
       - общая сумма расходов;
       - рассчитанный кешбэк (1 рубль за каждые 100 рублей расходов).

    3. Топ-5 транзакций с наибольшими расходами:
       - дата;
       - сумма;
       - категория;
       - описание.

    4. Курсы валют, выбранные пользователем, относительно рубля.

    5. Стоимость акций из списка предпочтений пользователя (из индекса S&P500).
    :param date: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'.
    :return: JSON-строка с объединёнными данными по приветствию, картам, топ 5 транзакциям, валютам и акциям.
    """

    logger.info(f"Function execution started with date: %s", date)
    try:
        greeting = get_greeting(date)
        logger.debug("The greeting has been formed.")

        start_date, end_date = get_month_range(date)
        logger.debug("Date range for filtering: %s - %s", start_date, end_date)

        df_transactions = load_operations(PATH)
        logger.info("Transactions successfully loaded. Total rows, columns: %s", df_transactions.shape)

        df_transact_period = df_transactions.loc[(df_transactions["Дата операции"] >= start_date) &
                                             (df_transactions["Дата операции"] <= end_date)]
        logger.debug("Transactions filtered for period. Rows after filter: %d", len(df_transact_period))

        cards = get_cards_expenses_and_cashback(df_transact_period)
        logger.debug("Transactions are grouped by the Card Number category and the total amount spent across "
                     "these categories is calculated.")

        top_transactions = get_top_transactions(df_transact_period)
        logger.debug("Top 5 transactions selected.")

        user_currencies, user_stocks = get_user_settings()
        logger.info("User settings loaded. Currencies: %s, Stocks: %s", user_currencies, user_stocks)

        currency_rates = get_currency_rates(user_currencies)
        logger.debug("Currency rates fetched: %s", currency_rates)

        stock_prices = get_stock_prices(user_stocks)
        logger.debug("Stock prices fetched: %s", stock_prices)

        for stock in stock_prices:
            stock["price"] = round(stock["price"] * currency_rates[0]["rate"], 2)

        final_result = {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }

        logger.info("All data assembled successfully.")
        return json.dumps(final_result, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        logger.error("Error: Not such file.")
        error_message = {"Error": "Not such file."}
    except requests.exceptions.RequestException as req_err:
        logger.error("[HTTP Error]: %s", req_err)
        error_message = {"Error": f"[HTTP Error]: {req_err}"}
    except json.JSONDecodeError as json_err:
        logger.error("JSON Decode Error: %s", json_err)
        error_message = {"Error": f"JSON Decode Error: {json_err}"}
    except Exception as e:
        logger.exception("Unexpected error during home_page execution.")
        error_message = {"Error": f"Unexpected error: {e}"}

    return json.dumps(error_message, indent=4, ensure_ascii=False)
