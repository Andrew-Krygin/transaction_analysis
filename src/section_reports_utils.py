from datetime import datetime

import pandas as pd

from src.config import PATH
from src.constants import CATEGORIES, FORMATS


def validate_category(categories: dict) -> str:
    """
    Функция возвращает категорию, выбранную пользователем.
    :param categories: Словарь с категориями.
    :return: Категория, выбранная пользователем.
    """
    while True:
        try:
            choice = int(input("Пользователь: "))
            if 0 < choice <= len(categories):
                category: str = categories[choice]
                return category
            else:
                print("Такой категории нет! Попробуйте снова.")
        except ValueError:
            print("Такой категории нет! Попробуйте снова.")


def get_date() -> None | str:
    """
    Функция возвращает дату если пользователь укажет или None.
    :return: Дата или None.
    """
    date = None

    print(
        """
Укажите дату от которой вы хотите посмотреть траты по заданной категории за последние три месяца.
Если не укажете, поиск начнется от текущей даты."""
    )

    if user_input := input("Введите дату/Enter чтобы пропустить: "):
        while True:
            for fmt in FORMATS:
                try:
                    date = datetime.strptime(user_input, fmt).strftime("%d.%m.%Y")
                    return date
                except ValueError:
                    continue
            print("Неверный формат даты. Попробуйте снова (например, 27.06.2025).")
            user_input = input("Введите дату/Enter чтобы пропустить: ")
    return date


def show_categories(list_categories: list[str]) -> None:
    """
    Функция показывает пользователю список категорий для выбора.
    :param list_categories: Список.
    :return: None.
    """
    print("Выберите категорию, информацию о которой вы хотите получить за 3 месяца:")
    print("-" * 115)

    columns = 4
    cell_width = 30  # Ширина одного столбца — можно настроить под себя

    for i, category in enumerate(list_categories, start=1):
        entry = f"{i}. {category}"
        print(f"{entry:<{cell_width}}", end="")  # выравнивание по левому краю
        if i % columns == 0:
            print()
    if len(list_categories) % columns != 0:
        print()


def get_data_reports() -> tuple:
    """
    Функция возвращает DataFrame, категорию и дату, от которой нужно осуществлять поиск трат за трехмесячные период.
    :return: DataFrame, категория и дата.
    """
    df_transactions = pd.read_excel(PATH)
    df_transactions = df_transactions[df_transactions["Сумма платежа"] < 0]
    list_transact = list(df_transactions["Категория"].dropna().unique())

    show_categories(list_transact)
    user_choice_category = validate_category(CATEGORIES)

    date_spending_by_category = get_date()
    return df_transactions, user_choice_category, date_spending_by_category
