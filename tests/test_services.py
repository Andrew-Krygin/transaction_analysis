from unittest.mock import MagicMock, patch

import pytest

from src.services import cat_upper_cashback, read_transactions
from tests.tests_data.data_for_services import LIST_TRANSACTION


class TestServices:
    def test_valid_read_transactions(self) -> None:
        with patch("src.services.pd.read_excel") as mock_read:
            mock_df = MagicMock()
            mock_df.to_dict.return_value = [
                {"Дата операции": "12.02.2024 11:00:00", "Категория": "еда", "Сумма": 100},
                {"Дата операции": "10.04.2024 09:00:00", "Категория": "Еда", "Сумма": 200},
            ]

            mock_read.return_value = mock_df
            result = read_transactions("fake_path.xlsx")
            assert result == mock_df.to_dict.return_value

    def test_read_transactions_invalid_path(self) -> None:
        with pytest.raises(TypeError):
            read_transactions(["fake_path.xlsx"])  # type: ignore

    def test_read_transactions_file_not_found(self) -> None:
        with patch("src.services.pd.read_excel") as mock_read:
            mock_read.side_effect = FileNotFoundError
            with pytest.raises(FileNotFoundError):
                read_transactions("fake_path.xlsx")

            mock_read.side_effect = Exception
            with pytest.raises(Exception):
                read_transactions("fake_path.xlsx")

    def test_get_cat_upper_cashback(self) -> None:
        with patch("json.dumps", return_value=[{1: "hellow"}, {2: "world!"}]):
            result = cat_upper_cashback(LIST_TRANSACTION, 10, 2024)
            assert result == [{1: "hellow"}, {2: "world!"}]

    def test_get_cat_upper_cashback_exceptions(self) -> None:
        with pytest.raises(TypeError):
            cat_upper_cashback(LIST_TRANSACTION, "10", 2024)  # type: ignore

        with patch("json.dumps", side_effect=Exception):
            with pytest.raises(Exception):
                cat_upper_cashback(LIST_TRANSACTION, 10, 2024)
