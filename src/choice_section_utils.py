from src.constants import CHOICE_MENU, SECTIONS


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
