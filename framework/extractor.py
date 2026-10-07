import csv
from pathlib import Path


def extract_csv(source_path, logger):
    """
    Extract records from a CSV source.

    Args:
        source_path: Path to the source CSV file.
        logger: Pipeline logger.

    Returns:
        list: Source records represented as dictionaries.
    """
    source_path = Path(source_path)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_path}"
        )

    logger.info(
        "Starting extraction from %s",
        source_path
    )

    with open(
        source_path,
        mode="r",
        encoding="utf-8",
        newline=""
    ) as source_file:
        reader = csv.DictReader(source_file)
        records = list(reader)

    logger.info(
        "Extracted %s records from %s",
        len(records),
        source_path
    )

    return records
