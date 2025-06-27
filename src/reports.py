import logging
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.decorators import log

logger = logging.getLogger(__name__)


@log("spending_by_category.log")
def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    :param transactions: DataFrame с транзакциями.
    :param category: Название категории.
    :param date: Опциональная дата. Если дата не передана, то берется текущая дата.
    :return: DataFrame.
    """
    logger.info("The function spending_by_category started. Category: %s, Date: %s", category, date)
    if not isinstance(transactions, pd.DataFrame):
        logger.error("Error! | Type: %s", type(transactions).__name__)
        raise TypeError(f"Transactions must be DataFrame, got {type(transactions)}")

    try:
        logger.debug("Convert all dates of the dataframe into a datetime object.")
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], errors="coerce", format="%d.%m.%Y %H:%M:%S"
        )

        logger.debug("Dropping rows with invalid dates (NaT).")
        transactions_clean = transactions.dropna(subset=["Дата операции"])

        transactions_clean["Категория"] = transactions_clean["Категория"].str.strip().str.title()
        logger.info("Preprocessing completed successfully.")
    except Exception as e:
        logger.error("Error:%s", e, exc_info=True)
        raise

    if date is None:
        dt_date = datetime.now()
    elif isinstance(date, str):
        try:
            dt_date = datetime.strptime(date, "%d.%m.%Y")
            dt_date = dt_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            logger.error("The date must be in the format DD.MM.YYYY, for example '12.01.2024'")
            raise ValueError("The date must be in the format DD.MM.YYYY, for example '12.01.2024'")
    else:
        logger.error("Invalid type for date: %s", type(date).__name__)
        raise TypeError("The 'date' parameter must be a string in format DD.MM.YYYY or None")

    logger.debug("Filtering transactions from %s to %s", dt_date - relativedelta(months=3), dt_date)
    start_date = dt_date - relativedelta(months=3)

    spending = transactions_clean.loc[
        (transactions_clean["Дата операции"] >= start_date)
        & (transactions_clean["Дата операции"] <= dt_date)
        & (transactions_clean["Категория"] == category.title())
    ]
    if spending.empty:
        logger.info(
            "No transactions found for category '%s' from %s to %s.",
            category,
            start_date.strftime("%Y-%m-%d"),
            dt_date.strftime("%Y-%m-%d"),
        )

    logger.info("Returning filtered transactions.")
    return spending
