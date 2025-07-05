import pandas as pd
import pytest


# Фикстура c DataFrame.
@pytest.fixture
def dataframe_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": [
                "12.02.2024 11:00:00",
                "10.04.2024 09:00:00",
                "15.05.2024 14:00:00",
                "10.06.2024 09:00:00",
                "01.01.2024 11:00:00",
            ],
            "Категория": ["еда", "Еда", " еда ", "еда", "Супермаркеты"],
            "Сумма": [100, 200, 300, 400, 7543],
        }
    )


@pytest.fixture
def sample_choice_menu() -> dict:
    return {
        "Главная": {
            1: "1 категория",
            2: "1 категория",
            3: "1 категория",
            4: "1 категория",
        },
        "Сервисы": {1: "1 категория"},
        "Отчеты": {1: "1 категория"},
    }


@pytest.fixture
def sample_df_1() -> pd.DataFrame:
    data = {"Сумма платежа": [-100, 200, -50], "Категория": ["Еда", "Зарплата", "Транспорт"]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_df_2() -> pd.DataFrame:
    data = {"Дата операции": pd.to_datetime(["2025-06-01", "2025-06-15", "2025-07-01"]), "Сумма": [-100, -50, 200]}
    return pd.DataFrame(data)
