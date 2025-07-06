from unittest.mock import patch

import pandas as pd
import pytest

from src.constants import CATEGORIES
from src.section_reports_utils import get_data_reports, show_categories, validate_category
from tests.tests_data.data_for_section_reports_utils import SAMPLE_CATEGORIES, SAMPLE_LIST_CATEGORIES


class TestSectionReportsUtils:
    @pytest.mark.parametrize(
        "inputs, res",
        [
            ("1", "Супермаркеты"),
            ("2", "Различные товары"),
            ("46", "Duty Free"),
        ],
    )
    def test_validate_category(self, inputs: str, res: int) -> None:
        with patch("builtins.input", return_value=inputs) as mock_input:
            result = validate_category(CATEGORIES)
            assert result == res
            mock_input.assert_called()

    @pytest.mark.parametrize("inputs, res", [(["-1", "0", "50", "24"], "Одежда и обувь")])
    def test_validate_category_absent(self, capsys: pytest.CaptureFixture, inputs: list[str], res: str) -> None:
        with patch("builtins.input", side_effect=inputs) as mock_input:
            result = validate_category(CATEGORIES)
            captured = capsys.readouterr()
            assert result == res
            assert "Такой категории нет!" in captured.out
            mock_input.assert_called()

    def test_show_category(self, capsys: pytest.CaptureFixture) -> None:
        show_categories(SAMPLE_LIST_CATEGORIES)
        captured = capsys.readouterr()
        assert SAMPLE_CATEGORIES.strip() == captured.out.strip()

    def test_get_data_reports(self, sample_df_1: pd.DataFrame) -> None:
        with (
            patch("src.section_reports_utils.pd.read_excel", return_value=sample_df_1) as mock_read_excel,
            patch("src.section_reports_utils.show_categories") as mock_show_categories,
            patch("src.section_reports_utils.validate_category", return_value="Еда") as mock_validate_category,
            patch("src.section_reports_utils.get_date", return_value="2024-06-01") as mock_get_date,
        ):
            df, category, date = get_data_reports()

            # Проверяем, что Excel прочитан
            mock_read_excel.assert_called_once()

            # Проверяем фильтрацию: только отрицательные суммы
            assert (df["Сумма платежа"] >= 0).sum() == 0

            # Проверяем вызов show_categories с уникальными категориями
            expected_categories = ["Еда", "Транспорт"]
            mock_show_categories.assert_called_once_with(expected_categories)

            # Проверяем validate_category
            mock_validate_category.assert_called_once()

            # Проверяем get_date
            mock_get_date.assert_called_once()

            # Проверяем возвращаемое значение
            assert category == "Еда"
            assert date == "2024-06-01"
