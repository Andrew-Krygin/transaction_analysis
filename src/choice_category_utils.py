from src.constants import CATEGORY, CHOICE_MENU


def get_choice_category_in_section(sect: str) -> int:
    print("Выберите категорию: ")
    for i, category in enumerate(CATEGORY[sect], start=1):
        print(f"{i}. {category}")
    print()

    user_choice = validate_category_in_section(CHOICE_MENU, sect)

    return user_choice


def validate_category_in_section(sections_menu: dict, section: str) -> int:
    """
    Функция возвращает выбор категории пользователя из указанного раздела меню и обрабатывает возможные ошибки ввода.
    :return: Корректный выбор пользователя
    """
    while True:
        try:
            choice = int(input("Пользователь: "))
            if 0 < choice <= len(sections_menu[section]):
                return choice
            else:
                print("Такой категории нет! Попробуйте снова.")
        except ValueError:
            print("Такой категории нет! Попробуйте снова.")
