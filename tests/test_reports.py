from pathlib import Path

import pandas as pd
import pytest

from src.decorators import log
from src.reports import spending_by_category


class TestReports:
    def test_valid_spending_by_category(self, dataframe_transactions: pd.DataFrame) -> None:
        result = spending_by_category(dataframe_transactions, category="Еда", date="10.06.2024")
        assert len(result) == 3

    def test_spending_by_category_default_date(self, dataframe_transactions: pd.DataFrame) -> None:
        result = spending_by_category(dataframe_transactions, category="Еда")
        assert len(result) == 0

    @pytest.mark.parametrize(
        "category, date",
        [
            (None, "10.06.2024"),
            ("Супермаркеты", "Алеша"),
        ],
    )
    def test_invalid_spending_by_category(
        self, dataframe_transactions: pd.DataFrame, category: str, date: str
    ) -> None:
        with pytest.raises(Exception):
            spending_by_category(dataframe_transactions, category, date)

    def test_spending_by_category_empty_dataframe(self) -> None:
        with pytest.raises(Exception):
            spending_by_category(pd.DataFrame(), category="Еда", date="10.06.2024")


class TestLogDecorators:
    def test_valid_log_decorator(self, tmp_path: Path, dataframe_transactions: pd.DataFrame) -> None:
        log_file = tmp_path / "test_log.log"

        @log(log_file)  # type: ignore
        def get_df(df: pd.DataFrame) -> pd.DataFrame:
            return df.head(1)

        get_df(dataframe_transactions)
        assert log_file.exists()

        content = log_file.read_text()
        assert "Function get_df finished successfully with result" in content

    def test_except_log_decorator(self, tmp_path: Path, dataframe_transactions: pd.DataFrame) -> None:
        log_file = tmp_path / "test_log.log"

        @log(log_file)  # type: ignore
        def filter_df(df: pd.DataFrame) -> pd.DataFrame:
            raise Exception("Test exception")

        with pytest.raises(Exception):
            assert filter_df(dataframe_transactions)
        assert log_file.exists()

        content = log_file.read_text()
        assert "Error in filter_df" in content
