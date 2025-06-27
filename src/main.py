import json

import requests

from src.choice_category_utils import get_choice_category_in_section
from src.choice_section_utils import get_choice_section
from src.constants import CHOICE_MENU
from src.section_reports_utils import get_data_reports
from src.utils import show_menu
from src.views import get_greeting, get_user_dashboard


def main() -> None:
    """
    Запускает интерактивное меню пользователя, обрабатывает выбор,
    получает и выводит данные по разделам, обрабатывает возможные ошибки.
    :return: None.
    """
    try:
        date = "23.06.2019 23:32:12"
        show_menu()

        section = get_choice_section()
        section_category = get_choice_category_in_section(section)

        choice = CHOICE_MENU[section][section_category]
        if section == "Главная":
            dashboard_data = json.loads(get_user_dashboard(date))
            greeting = dashboard_data.get("greeting")
            result = dashboard_data.get(choice)
        elif section == "Сервисы":
            greeting = get_greeting(date)
            result = choice()
        else:
            df_transact, user_choice, date_spending_by_category = get_data_reports()
            greeting = get_greeting(date)
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
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
