import json

import requests

from src.choice_category_utils import get_choice_category_in_section
from src.choice_section_utils import call_choice_main, get_choice_section
from src.constants import CHOICE_MENU, SECTION_MAIN, SECTION_SERVICES
from src.section_reports_utils import get_data_reports
from src.utils import show_menu
from src.views import get_greeting


def main() -> None:
    """
    Запускает интерактивное меню пользователя, обрабатывает выбор,
    получает и выводит данные по разделам, обрабатывает возможные ошибки.
    :return: None.
    """
    try:
        date = "23.06.2019 23:32:12"
        show_menu()

        section: str = get_choice_section()
        section_category: int = get_choice_category_in_section(section)

        greeting: str = get_greeting(date)

        if section == SECTION_MAIN:
            result = call_choice_main(section, section_category, date)
        elif section == SECTION_SERVICES:
            choice = CHOICE_MENU[section][section_category]
            result = choice()
        else:
            df_transact, user_choice, date_spending_by_category = get_data_reports()
            choice = CHOICE_MENU[section][section_category]
            result = choice(df_transact, user_choice, date_spending_by_category)

        print()
        print(f"{greeting} Пользователь!\nОтвет: ", result, sep="\n")
    except TypeError as e:
        print(f"Ошибка: {e}")
    except requests.exceptions.RequestException as req_err:
        print(f"[HTTP Error]: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"[JSON Decode Error]: {json_err}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except KeyError as e:
        print(f"Неизвестный раздел или категория: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
