from typing import Any

from src.config import PATH
from src.constants import CHOICE_MENU, SECTION_MAIN, SECTIONS
from src.utils import get_month_range, get_user_settings, load_operations


def get_choice_section() -> str:
    """
    Функция запрашивает у пользователя раздел приложения который он хочет использовать.
    :return: Название раздела.
    """

    print("Выберите раздел: ")
    for i, section in enumerate(CHOICE_MENU.keys(), start=1):
        print(f"{i}. {section}")

    print()
    user_choice = validate_sections()

    return SECTIONS[user_choice]


def validate_sections() -> int:
    """
    Функция запрашивает у пользователя выбор раздела меню (1–3) и обрабатывает возможные ошибки ввода.
    :return: Корректный выбор пользователя (целое число от 1 до 3)
    """
    while True:
        try:
            choice = int(input("Пользователь: "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Такого раздела нет. Выберите раздел 1-3.")
        except ValueError:
            print("Такого раздела нет. Выберите раздел 1-3.")


def call_choice_main(section: str, section_category: int, date: str) -> Any:
    """
    Выполняет выбор и вызов соответствующей функции из меню для раздела "Главная" с передачей нужных параметров.
    :param section: Название раздела, ожидается "Главная".
    :param section_category: Выбранная категория внутри раздела "Главная" (целое число).
    :param date: Дата в строковом формате, например, "23.06.2019 23:32:12", для определения периода анализа.
    :return: Результат вызова функции из CHOICE_MENU, тип зависит от конкретной функции.
    :raises KeyError: Если категория section_category не предусмотрена в разделе "Главная".
    """
    if section == SECTION_MAIN:
        # Получаем диапазон дат на основе переданной строки `date`.
        start_date, end_date = get_month_range(date)

        # Загружаем транзакции и фильтруем их по периоду.
        df_transactions = load_operations(PATH)
        df_transact_period = df_transactions.loc[
            (df_transactions["Дата операции"] >= start_date) & (df_transactions["Дата операции"] <= end_date)
        ]

        # Загружаем пользовательские настройки (валюты и акции).
        user_currencies, user_stocks = get_user_settings()

        # Вызываем нужную функцию из CHOICE_MENU в зависимости от категории раздела.
        choice = CHOICE_MENU[section][section_category]

        if section_category in (1, 2):
            return choice(df_transact_period)
        elif section_category == 3:
            return choice(user_currencies)
        elif section_category == 4:
            return choice(user_stocks)
        else:
            raise KeyError
