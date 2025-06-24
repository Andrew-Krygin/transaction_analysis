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
