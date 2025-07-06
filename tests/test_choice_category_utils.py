from unittest.mock import patch

import pytest

from src.choice_category_utils import get_choice_category_in_section, validate_category_in_section


class TestChoiceCategoryUtils:
    @pytest.mark.parametrize(
        "input_section, inputs, res",
        [
            ("Главная", 4, 4),
            ("Главная", 3, 3),
            ("Сервисы", 1, 1),
            ("Отчеты", 1, 1),
        ],
    )
    def test_get_choice_category_in_section(self, input_section: str, inputs: int, res: int) -> None:
        with patch("src.choice_category_utils.validate_category_in_section", return_value=inputs) as mock_validate:
            result = get_choice_category_in_section(input_section)
            assert result == res
            mock_validate.assert_called()

    @pytest.mark.parametrize(
        "input_section, inputs, res",
        [
            ("Главная", "4", 4),
            ("Главная", "3", 3),
            ("Сервисы", "1", 1),
            ("Отчеты", "1", 1),
        ],
    )
    def test_validate_category_in_section(
        self, sample_choice_menu: dict, input_section: str, inputs: str, res: int
    ) -> None:
        with patch("builtins.input", return_value=inputs):
            result = validate_category_in_section(sample_choice_menu, input_section)
            assert result == res

    @pytest.mark.parametrize(
        "input_section, inputs, res",
        [
            ("Главная", ["0", "-1", "6", "3"], 3),
            ("Главная", ["Ghb", "", "1"], 1),
            ("Сервисы", ["0", "-1", "2", "1"], 1),
            ("Сервисы", ["Ghb", "", "1"], 1),
            ("Отчеты", ["0", "-1", "2", "1"], 1),
            ("Отчеты", ["Ghb", "", "1"], 1),
        ],
    )
    def test_validate_category_in_section_exception(
        self, capsys: pytest.CaptureFixture, sample_choice_menu: dict, input_section: str, inputs: list[int], res: int
    ) -> None:
        with patch("builtins.input", side_effect=inputs):
            result = validate_category_in_section(sample_choice_menu, input_section)
            captured = capsys.readouterr()
            assert "Такой категории нет!" in captured.out
            assert result == res
