from typing import Any, Callable

from src.reports import spending_by_category
from src.services import get_upper_cashback
from src.views import get_cards_expenses_and_cashback, get_currency_rates, get_stock_prices, get_top_transactions

SECTION_MAIN = "Главная"
SECTION_SERVICES = "Сервисы"


CHOICE_MENU: dict[str, dict[int, Callable[..., Any]]] = {
    "Главная": {
        1: lambda df_transact_period: get_cards_expenses_and_cashback(df_transact_period),
        2: lambda df_transact_period: get_top_transactions(df_transact_period),
        3: lambda user_currencies: get_currency_rates(user_currencies),
        4: lambda user_stocks: get_stock_prices(user_stocks),
    },
    "Сервисы": {
        1: lambda: get_upper_cashback(),
    },
    "Отчеты": {
        1: lambda df_transactions, category, date: spending_by_category(df_transactions, category, date),
    },
}

SECTIONS = {1: "Главная", 2: "Сервисы", 3: "Отчеты"}

CATEGORY = {
    "Главная": ["Информация по картам", "Топ-5 самых крупных трат", "Курсы валют", "Цены на акции"],
    "Сервисы": ["Выгодные категории для повышенного кешбэка (за выбранный месяц)"],
    "Отчеты": ["Расходы по категории за последние 3 месяца"],
}

CATEGORIES = {
    1: "Супермаркеты",
    2: "Различные товары",
    3: "Переводы",
    4: "Каршеринг",
    5: "Канцтовары",
    6: "Ж/д билеты",
    7: "Фастфуд",
    8: "Дом и ремонт",
    9: "Аптеки",
    10: "Связь",
    11: "Такси",
    12: "Транспорт",
    13: "Цветы",
    14: "Развлечения",
    15: "Госуслуги",
    16: "Местный транспорт",
    17: "Другое",
    18: "Топливо",
    19: "Услуги банка",
    20: "Сервис",
    21: "ЖКХ",
    22: "Детские товары",
    23: "Косметика",
    24: "Одежда и обувь",
    25: "НКО",
    26: "Электроника и техника",
    27: "Наличные",
    28: "Сувениры",
    29: "Мобильная связь",
    30: "Медицина",
    31: "Фото и видео",
    32: "Онлайн-кинотеатры",
    33: "Авиабилеты",
    34: "Образование",
    35: "Рестораны",
    36: "Частные услуги",
    37: "Красота",
    38: "Турагентства",
    39: "Книги",
    40: "Отели",
    41: "Кино",
    42: "Спорттовары",
    43: "Автоуслуги",
    44: "Финансы",
    45: "Искусство",
    46: "Duty Free",
}


FORMATS = [
    "%Y-%m-%d",  # 2025-06-27
    "%Y.%m.%d",  # 2025.06.27
    "%Y/%m/%d",  # 2025/06/27
    "%Y %m %d",  # 2025 06 27
    "%d.%m.%Y",  # 27.06.2025
    "%d/%m/%Y",  # 27/06/2025
    "%d-%m-%Y",  # 27-06-2025
    "%d %m %Y",  # 27 06 2025
    "%d.%m.%y",  # 27.06.25
    "%d/%m/%y",  # 27/06/25
]
