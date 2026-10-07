import logging
from pathlib import Path


LOG_DIRECTORY = Path("output/logs")


def get_logger(
    logger_name="data_engineering_framework",
    log_level=logging.INFO
):
    """
    Create a reusable logger that writes messages
    to both the console and a log file.
    """

    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_DIRECTORY / "pipeline.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
