import json
import math
from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

import pandas as pd

from src.config import PATH
from src.settings_logger import setup_logger

logger = setup_logger(__name__, "DEBUG", "services.log")


def read_transactions(path_to_file: str) -> list[dict]:
    """
    Функция читает файл формата exel и возвращает список транзакций.
    :param path_to_file: Путь к файлу формата exel.
    :return: Список транзакций.
    """
    logger.info("The function read_transactions started. Path to file: %s", path_to_file)
    if not isinstance(path_to_file, str):
        logger.error("Error! | Type: %s", type(path_to_file).__name__)
        raise TypeError(f"The path must be a str, got {type(path_to_file)}.")
    try:
        logger.info("Read transactions from an excel file.")
        df_transactions = pd.read_excel(path_to_file)

        logger.info("Reading was successful! Return: %d", len(df_transactions))
        return df_transactions.to_dict(orient="records")
    except FileNotFoundError:
        logger.error("File not found: %s", path_to_file)
        raise
    except Exception:
        logger.exception("Error! Unexpected error during read_transactions execution.")
        raise


def cat_upper_cashback(list_transactions: list[dict], month: int, year: int) -> str:
    """
    Функция анализирует, какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка.
    :param list_transactions: Список транзакций.
    :param month: Месяц в котором нужно провести анализ.
    :param year: Год в котором нужно провести анализ.
    :return: Json с анализом, сколько на каждой категории можно заработать кешбэка.
    """
    logger.info("The function cat_upper_cashback started. Month: %d, Year: %d", month, year)
    if not isinstance(list_transactions, list):
        logger.error("Error! | Type: %s", type(list_transactions).__name__)
        raise TypeError(f"The transactions must be a list, got {type(list_transactions)}")

    upper_cashback: DefaultDict[str, int] = defaultdict(int)

    logger.debug("Iterating through transactions one by one.")
    for transact in list_transactions:
        if not isinstance(transact, dict):
            logger.error("Error! | Type: %s", type(transact).__name__)
            raise TypeError(f"The transact must be a dict, got {type(transact)}")

        raw_date = transact.get("Дата операции")
        if not isinstance(raw_date, str):
            continue

        try:
            date = datetime.strptime(raw_date, "%d.%m.%Y %H:%M:%S")
        except (TypeError, ValueError):
            logger.warning("Error converting date:%s. Skipping date.", transact.get("Дата операции"))
            continue

        cat = transact.get("Категория")
        cashback = transact.get("Кэшбэк")

        if isinstance(cashback, float) and math.isnan(cashback):
            cashback = 0.0

        if pd.notna(cat) and isinstance(cashback, (int, float)):
            if date.month == month and date.year == year:
                upper_cashback[cat] += int(cashback)

    try:
        logger.info("Let's convert the data into json format.")
        upper_cashback_json = json.dumps(upper_cashback, ensure_ascii=False, indent=4)

        logger.info(
            "The function get_cat_upper_cashback completed successfully. Total categories: %d", len(upper_cashback)
        )
        logger.debug("Result: %s", upper_cashback_json)

        return upper_cashback_json
    except Exception:
        logger.exception("Unexpected error during get_cat_upper_cashback execution.")
        raise


def get_upper_cashback() -> str:
    """
    Функция возвращает выгодные категории кэшбэка за указанный месяц.
    :return: Список категорий повышенного кэшбэка.
    """
    month = int(input("Введите месяц для поиска: "))
    year = int(input("Введите год для поиска: "))
    lst_transactions = read_transactions(PATH)

    upper_cashback = cat_upper_cashback(lst_transactions, month, year)
    return upper_cashback
