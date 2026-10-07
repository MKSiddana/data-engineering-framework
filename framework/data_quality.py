from collections import Counter


def validate_required_columns(records, required_columns):
    """
    Verify that every required column exists in the dataset.
    """
    if not records:
        return []

    available_columns = set(records[0].keys())

    return [
        column
        for column in required_columns
        if column not in available_columns
    ]


def find_null_records(records, required_columns):
    """
    Identify records containing null or empty values
    in required columns.
    """
    invalid_records = []

    for record in records:
        for column in required_columns:
            value = record.get(column)

            if value is None or str(value).strip() == "":
                invalid_records.append(record)
                break

    return invalid_records


def find_duplicate_records(records, unique_columns):
    """
    Identify duplicate records using configured
    business-key columns.
    """
    keys = [
        tuple(record.get(column) for column in unique_columns)
        for record in records
    ]

    key_counts = Counter(keys)

    duplicate_keys = {
        key
        for key, count in key_counts.items()
        if count > 1
    }

    return [
        record
        for record, key in zip(records, keys)
        if key in duplicate_keys
    ]


def run_data_quality_checks(records, config):
    """
    Execute configuration-driven data-quality checks.
    """
    dq_config = config["data_quality"]

    required_columns = dq_config.get(
        "required_columns",
        []
    )

    unique_columns = dq_config.get(
        "unique_columns",
        []
    )

    missing_columns = validate_required_columns(
        records,
        required_columns
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    null_records = []

    if not dq_config.get("allow_nulls", True):
        null_records = find_null_records(
            records,
            required_columns
        )

    duplicate_records = find_duplicate_records(
        records,
        unique_columns
    )

    passed = (
        len(null_records) == 0
        and len(duplicate_records) == 0
    )

    results = {
        "passed": passed,
        "total_records": len(records),
        "null_record_count": len(null_records),
        "duplicate_record_count": len(duplicate_records)
    }

    return results
