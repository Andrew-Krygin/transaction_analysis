from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from src.choice_section_utils import call_choice_main, get_choice_section, validate_sections


class TestChoiceSectionUtils:
    @pytest.mark.parametrize(
        "return_value, res",
        [
            (1, "Главная"),
            (2, "Сервисы"),
            (3, "Отчеты"),
        ],
    )
    def test_get_choice_section(self, return_value: int, res: str) -> None:
        with patch("src.choice_section_utils.validate_sections", return_value=return_value) as mock_validate:
            result = get_choice_section()
            assert result == res
            mock_validate.assert_called()

    @pytest.mark.parametrize(
        "inputs, res",
        [
            ("1", 1),
            ("2", 2),
            ("3", 3),
        ],
    )
    def test_validate_sections(self, inputs: str, res: int) -> None:
        with patch("builtins.input", return_value=inputs) as mock_input:
            result = validate_sections()
            assert result == res
            mock_input.assert_called_once()

    @pytest.mark.parametrize(
        "inputs, res",
        [
            (["0", "-1", "4", "1"], 1),
            (["-3", "4", "5", "2"], 2),
            (["10", "-8", "0", "3"], 3),
            (["Ghb", "", "1"], 1),
        ],
    )
    def test_validate_sections_exception(self, capsys: pytest.CaptureFixture, inputs: list[str], res: int) -> None:
        with patch("builtins.input", side_effect=inputs) as mock_input:
            result = validate_sections()
            captured = capsys.readouterr()
            assert "Выберите раздел 1-3." in captured.out
            assert result == res
            mock_input.assert_called()

    def test_call_choice_main_category_1(self, sample_df_2: pd.DataFrame) -> None:
        with (
            patch(
                "src.choice_section_utils.get_month_range", return_value=("2025-06-01", "2025-06-30")
            ) as mock_get_range,
            patch("src.choice_section_utils.load_operations", return_value=sample_df_2) as mock_load_ops,
            patch(
                "src.choice_section_utils.get_user_settings", return_value=(["USD", "EUR"], ["AAPL", "TSLA"])
            ) as mock_user_settings,
            patch.dict(
                "src.choice_section_utils.CHOICE_MENU", {"Главная": {1: MagicMock(return_value="result_category_1")}}
            ) as mock_menu,
        ):
            result = call_choice_main("Главная", 1, "2025-06-01")

            mock_get_range.assert_called_once_with("2025-06-01")
            mock_load_ops.assert_called_once()
            mock_user_settings.assert_called_once()

            filtered = sample_df_2[
                (sample_df_2["Дата операции"] >= "2025-06-01") & (sample_df_2["Дата операции"] <= "2025-06-30")
            ]
            choice_fn = mock_menu["Главная"][1]
            called_df = choice_fn.call_args[0][0]
            assert_frame_equal(called_df, filtered)

            assert result == "result_category_1"

    def test_call_choice_main_category_3(self, sample_df_2: pd.DataFrame) -> None:
        with (
            patch("src.choice_section_utils.get_month_range", return_value=("2025-06-01", "2025-06-30")),
            patch("src.choice_section_utils.load_operations", return_value=sample_df_2),
            patch("src.choice_section_utils.get_user_settings", return_value=(["USD", "EUR"], ["AAPL", "TSLA"])),
            patch.dict(
                "src.choice_section_utils.CHOICE_MENU", {"Главная": {3: MagicMock(return_value="result_category_3")}}
            ) as mock_menu,
        ):
            result = call_choice_main("Главная", 3, "2025-06-01")

            choice_fn = mock_menu["Главная"][3]
            choice_fn.assert_called_once_with(["USD", "EUR"])
            assert result == "result_category_3"

    def test_call_choice_main_invalid_category(self, sample_df_2: pd.DataFrame) -> None:
        with (
            patch("src.choice_section_utils.get_month_range", return_value=("2025-06-01", "2025-06-30")),
            patch("src.choice_section_utils.load_operations", return_value=sample_df_2),
            patch("src.choice_section_utils.get_user_settings", return_value=(["USD", "EUR"], ["AAPL", "TSLA"])),
            patch.dict("src.choice_section_utils.CHOICE_MENU", {"Главная": {1: MagicMock()}}),
        ):
            with pytest.raises(KeyError):
                call_choice_main("Главная", 5, "2025-06-01")
