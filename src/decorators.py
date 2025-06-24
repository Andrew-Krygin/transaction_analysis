from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from src.settings_logger import setup_logger

P = ParamSpec("P")
R = TypeVar("R")


def log(file_name: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор для логирования вызова функции.

    Логирует:
        - начало выполнения функции;
        - переданные позиционные и именованные аргументы;
        - успешное завершение с результатом;
        - исключение, если оно возникает, с типом и трассировкой.

    :param file_name: Путь к лог-файлу. Если None, логи никуда не выводятся и не записываются.
    :return: Обернутая функция с логированием.
    """

    def log_decorator(func: Callable[P, R]) -> Callable[P, R]:
        module_name = getattr(func, "__module__", "unknown")
        logger = setup_logger(module_name, "INFO", file_name)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                logger.info("Function %s started with args %s and kwargs %s.", func.__name__, args, kwargs)
                result = func(*args, **kwargs)
                logger.info("Function %s finished successfully with result: %s", func.__name__, result)
                return result
            except Exception as e:
                logger.exception(
                    "Error in %s | Type: %s | Args: %s | Kwargs: %s", func.__name__, type(e).__name__, args, kwargs
                )
                raise

        return wrapper

    return log_decorator
