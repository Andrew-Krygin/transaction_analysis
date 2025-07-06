import json
from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import get_month_range, get_user_settings, load_operations
from tests.tests_data.data_for_utils import USERS_SETTINGS


class TestUtils:
    def test_load_operations(self, dataframe_transactions: pd.DataFrame) -> None:
        with patch("src.views.pd.read_excel", return_value=dataframe_transactions):
            with patch("src.views.pd.to_datetime", return_value=dataframe_transactions["Дата операции"]):
                result = load_operations("fake_path.xlsx")
                assert result.equals(dataframe_transactions)

    def test_load_operations_exceptions(self, dataframe_transactions: pd.DataFrame) -> None:
        # Ошибка при чтении файла Excel
        with patch("src.views.pd.read_excel", side_effect=Exception):
            with pytest.raises(Exception):
                load_operations("fake_path.xlsx")

        # Ошибка при преобразовании даты
        with patch("src.views.pd.read_excel", return_value=dataframe_transactions):
            with patch("src.views.pd.to_datetime", side_effect=Exception):
                with pytest.raises(Exception):
                    load_operations("fake_path.xlsx")

    def test_get_month_range(self) -> None:
        date_str = "29.11.2021 19:48:21"
        expected_end = datetime(2021, 11, 29, 19, 48, 21)
        expected_start = datetime(2021, 11, 1, 0, 0, 0)

        start_date, end_date = get_month_range(date_str)

        assert start_date == expected_start
        assert end_date == expected_end

    def test_get_user_settings(self) -> None:
        with patch("json.load", return_value=USERS_SETTINGS):
            res1, res2 = get_user_settings()
            assert res1 == ["USD", "EUR"]
            assert res2 == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_user_settings_exceptions(self, mock_read: Mock) -> None:
        with pytest.raises(FileNotFoundError):
            get_user_settings()
        mock_read.assert_called_once()

    def test_get_user_settings_json_exception(self) -> None:
        # Тест на проверку исключения json.JSONDecodeError
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "", 0)):
            with pytest.raises(json.JSONDecodeError):
                get_user_settings()

        # Тест на проверку исключения Exception
        with patch("json.load", side_effect=Exception):
            with pytest.raises(Exception):
                get_user_settings()
