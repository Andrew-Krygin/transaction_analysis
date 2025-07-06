import logging
from pathlib import Path


def setup_logger(
    name: str,
    level: str | int,
    log_file: str | None = None,
    fmt: str = "%(asctime)s [%(levelname)-5s] logger:%(name)s module:%(module)s func:%(funcName)s:%(lineno)d - %("
    "message)s",
) -> logging.Logger:
    """
    Универсальная настройка логгера.

    :param name: Имя логгера (обычно __name__)
    :param level: уровень логирования (по умолчанию INFO)
    :param log_file: путь к лог-файлу (если нужно логировать в файл)
    :param fmt: формат сообщения
    :return: настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    if log_file:
        logs_dir = Path(__file__).resolve().parent.parent / "logs"
        log_path = logs_dir / log_file

        file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
