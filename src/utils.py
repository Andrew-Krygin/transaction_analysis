import json
from datetime import datetime

import pandas as pd

from src.config import BASE_DIR
from src.settings_logger import setup_logger

logger = setup_logger(__name__, "DEBUG", "views.log")


# Функция выводит меню программы на экран.
def show_menu() -> None:
    """
    Функция выводит пункты меню на экран.
    :return: None.
    """
    print(
        """
                        Меню программы
-----------------------------------------------------------------
Главная:
1. Информация по картам
2. Топ-5 самых крупных трат
3. Курсы валют
4. Цены на акции

Сервисы:
1.Выгодные категории для повышенного кешбэка (за выбранный месяц)

Отчеты:
1.Расходы по категории за последние 3 месяца
-----------------------------------------------------------------
"""
    )


# Функция загружает данные из файла operations.xlsx
def load_operations(file_path: str) -> pd.DataFrame:
    """
    Функция загружает операции из Excel-файла.
    :param file_path: Путь к файлу.
    :return: Dataframe с транзакциями.
    """
    logger.info("The function load_operations started. File path: %s", file_path)

    logger.debug("Loading Dataframe.")
    df = pd.read_excel(file_path)

    logger.debug("Handling empty or nan values in Dataframe.")
    df = df.fillna("")

    logger.debug("Converting 'Дата операции' column to datetime objects.")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    logger.info("The function completed successfully! Return DateFrame shape (rows, columns): %s", df.shape)
    return df


# Функция возвращает диапазон от начала месяца до указанной даты.
def get_month_range(date: str) -> tuple[datetime, datetime]:
    """
    Функция возвращает диапазон от начала месяца до указанной даты.
    :param date: Дата.
    :return: Возвращает кортеж дат, от начала месяца до указанной даты.
    """
    logger.info("The function get_month_range started. Date: %s", date)

    logger.debug("Convert a date from type 'str' to a datetime object.")
    dt_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    logger.debug("Replacing day, hour, minute, second and microsecond to get the start of the month.")
    start_date = dt_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    logger.info("The function completed successfully! Return start_date - %s, date - %s", start_date, dt_date)
    return start_date, dt_date


# Функция для чтения настроек из файла user_settings.json
def get_user_settings() -> tuple[list, list]:
    """
    Функция читает настройки из файла user_settings.json.
    :return: Кортеж с данными.
    """
    logger.info("The function get_user_settings started.")
    try:
        logger.debug("The user_settings.json file is being read.")
        with open(f"{BASE_DIR}/data/user_settings.json", encoding="utf-8") as f:
            data = json.load(f)

            logger.info(
                "The function get_user_settings read the file successfully. Return user_currencies: %s, "
                "user_stocks: %s",
                data["user_currencies"],
                data["user_stocks"],
            )
            return data["user_currencies"], data["user_stocks"]
    except FileNotFoundError:
        logger.error("Error: Not such file.")
        raise
    except json.JSONDecodeError as json_err:
        logger.error("JSON Decode Error: %s", json_err)
        raise
    except Exception:
        logger.error("Unexpected error during get_user_settings execution.")
        raise
