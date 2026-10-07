import sqlite3
from pathlib import Path


def _quote_identifier(identifier):
    """
    Safely quote a SQLite table or column identifier.
    """
    return '"' + identifier.replace('"', '""') + '"'


def load_to_sqlite(
    records,
    target_config,
    unique_columns,
    logger
):
    """
    Load records into a SQLite target table.

    Existing records are updated using the configured
    unique business key.
    """
    if not records:
        logger.info("No records available to load.")
        return 0

    database_path = Path(target_config["path"])
    table_name = target_config["table"]

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    columns = list(records[0].keys())

    if not unique_columns:
        raise ValueError(
            "At least one unique column must be configured."
        )

    primary_key = unique_columns[0]

    if primary_key not in columns:
        raise ValueError(
            f"Unique column not found: {primary_key}"
        )

    quoted_table = _quote_identifier(table_name)

    column_definitions = []

    for column in columns:
        quoted_column = _quote_identifier(column)

        if column == primary_key:
            column_definitions.append(
                f"{quoted_column} TEXT PRIMARY KEY"
            )
        else:
            column_definitions.append(
                f"{quoted_column} TEXT"
            )

    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {quoted_table} (
            {", ".join(column_definitions)}
        )
    """

    quoted_columns = [
        _quote_identifier(column)
        for column in columns
    ]

    placeholders = ", ".join(
        "?" for _ in columns
    )

    update_columns = [
        column
        for column in columns
        if column != primary_key
    ]

    update_clause = ", ".join(
        f"{_quote_identifier(column)} = "
        f"excluded.{_quote_identifier(column)}"
        for column in update_columns
    )

    insert_sql = f"""
        INSERT INTO {quoted_table} (
            {", ".join(quoted_columns)}
        )
        VALUES ({placeholders})
        ON CONFLICT({_quote_identifier(primary_key)})
        DO UPDATE SET
            {update_clause}
    """

    connection = sqlite3.connect(database_path)

    try:
        connection.execute(create_table_sql)

        for record in records:
            values = [
                record.get(column)
                for column in columns
            ]

            connection.execute(
                insert_sql,
                values
            )

        connection.commit()

        logger.info(
            "Loaded %s records into %s.",
            len(records),
            table_name
        )

        return len(records)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
