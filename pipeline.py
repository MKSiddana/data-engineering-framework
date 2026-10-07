from framework.audit import (
    start_pipeline_audit,
    complete_pipeline_audit
)
from framework.config_loader import load_config
from framework.data_quality import run_data_quality_checks
from framework.extractor import extract_csv
from framework.loader import load_to_sqlite
from framework.logger import get_logger
from framework.retry import execute_with_retry


def run_pipeline():
    """
    Execute the configuration-driven data pipeline.
    """
    config = load_config()

    pipeline_config = config["pipeline"]
    source_config = config["source"]
    target_config = config["target"]
    dq_config = config["data_quality"]

    logger = get_logger(
        pipeline_config["name"]
    )

    audit = start_pipeline_audit(
        pipeline_config["name"]
    )

    source_count = 0
    processed_count = 0
    rejected_count = 0

    logger.info(
        "Pipeline started. Run ID: %s",
        audit["run_id"]
    )

    try:
        records = extract_csv(
            source_config["path"],
            logger
        )

        source_count = len(records)

        dq_results = run_data_quality_checks(
            records,
            config
        )

        logger.info(
            "Data quality results: %s",
            dq_results
        )

        rejected_count = (
            dq_results["null_record_count"]
            + dq_results["duplicate_record_count"]
        )

        if not dq_results["passed"]:
            raise ValueError(
                "Data quality validation failed."
            )

        processed_count = execute_with_retry(
            load_to_sqlite,
            pipeline_config["max_retries"],
            pipeline_config["retry_delay_seconds"],
            logger,
            records,
            target_config,
            dq_config["unique_columns"],
            logger
        )

        completed_audit = complete_pipeline_audit(
            audit=audit,
            status="SUCCESS",
            source_count=source_count,
            processed_count=processed_count,
            rejected_count=0
        )

        logger.info(
            "Pipeline completed successfully."
        )

        logger.info(
            "Audit metrics: %s",
            completed_audit
        )

    except Exception as error:
        complete_pipeline_audit(
            audit=audit,
            status="FAILED",
            source_count=source_count,
            processed_count=processed_count,
            rejected_count=rejected_count,
            error_message=str(error)
        )

        logger.exception(
            "Pipeline failed: %s",
            error
        )

        raise


if __name__ == "__main__":
    run_pipeline()
