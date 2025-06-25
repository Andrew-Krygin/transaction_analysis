from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.views import (get_cards_expenses_and_cashback, get_currency_rates, get_greeting, get_stock_prices,
                       get_top_transactions)


class TestViews:
    @pytest.mark.parametrize(
        "input_date, expected_res",
        [
            ("24.06.2025 07:15:00", "Доброе утро"),
            ("24.06.2025 03:15:00", "Доброй ночи"),
            ("24.06.2025 13:45:00", "Добрый день"),
            ("24.06.2025 19:00:00", "Добрый вечер"),
        ],
    )
    def test_get_greeting(self, input_date: str, expected_res: str) -> None:
        result = get_greeting(input_date)
        assert result == expected_res

    def test_get_greeting_exceptions(self) -> None:
        with patch("src.views.datetime", side_effect=TypeError):
            with pytest.raises(TypeError):
                get_greeting("date")

    def test_get_cards_expenses_and_cashback_single_card(self) -> None:
        df = pd.DataFrame({"Номер карты": ["****1234", "****1234", "****1234"], "Сумма платежа": [-100, -150, -50]})
        result = get_cards_expenses_and_cashback(df)
        assert result == [{"last_digits": "1234", "total_spent": 300.0, "cashback": 3.0}]

    def test_get_cards_expenses_and_cashback_multiple_cards(self) -> None:
        df = pd.DataFrame(
            {
                "Номер карты": ["****1234", "****5678", "****1234", "****5678"],
                "Сумма платежа": [-100, -200, -100, -200],
            }
        )
        result = get_cards_expenses_and_cashback(df)
        expected = [
            {"last_digits": "1234", "total_spent": 200.0, "cashback": 2.0},
            {"last_digits": "5678", "total_spent": 400.0, "cashback": 4.0},
        ]
        assert sorted(result, key=lambda x: x["last_digits"]) == expected

    def test_get_top_transactions_limit(self) -> None:
        df = pd.DataFrame(
            {
                "Дата операции": [datetime(2024, 1, i + 1) for i in range(3)],
                "Сумма платежа": [-100.0, -300.0, -200.0],
                "Категория": ["еда", "транспорт", "одежда"],
                "Описание": ["кушал", "ехал", "покупал"],
            }
        )
        result = get_top_transactions(df)
        assert result[0]["amount"] == 300.0
        assert len(result) == 3

    def test_get_top_transactions_exactly_five(self) -> None:
        df = pd.DataFrame(
            {
                "Дата операции": [datetime(2024, 1, i + 1) for i in range(6)],
                "Сумма платежа": [-100, -200, -300, -400, -500, -50],
                "Категория": ["1", "2", "3", "4", "5", "6"],
                "Описание": ["a", "b", "c", "d", "e", "f"],
            }
        )
        result = get_top_transactions(df)
        assert len(result) == 5
        assert result[0]["amount"] == 500.0
        assert result[-1]["amount"] == 100.0

    @patch("src.views.requests.get")
    def test_get_currency_rates_success(self, mock_get: Mock) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"USD": 0.011, "EUR": 0.010}}

        result = get_currency_rates(["USD", "EUR"])
        assert {"currency": "USD", "rate": round(1 / 0.011, 2)} in result
        assert {"currency": "EUR", "rate": round(1 / 0.010, 2)} in result

    @patch("src.views.requests.get")
    def test_get_currency_rates_missing_rates_field(self, mock_get: Mock) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        try:
            get_currency_rates(["USD"])
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "missing 'rates'" in str(e)

    @patch("src.views.requests.get")
    def test_get_stock_prices_success(self, mock_get: Mock) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {"data": [{"ticker": "AAPL", "price": 200.5}]},
            {"data": [{"ticker": "GOOGL", "price": 150.3}]},
        ]

        result = get_stock_prices(["AAPL", "GOOGL"])
        assert result == [{"stock": "AAPL", "price": 200.5}, {"stock": "GOOGL", "price": 150.3}]

    @patch("src.views.requests.get")
    def test_get_stock_prices_http_error(self, mock_get: Mock) -> None:
        mock_get.side_effect = Exception("API down")

        try:
            get_stock_prices(["AAPL"])
            assert False, "Expected exception"
        except Exception as e:
            assert "API down" in str(e)
