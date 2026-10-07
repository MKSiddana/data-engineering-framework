import time


def execute_with_retry(
    operation,
    max_retries,
    retry_delay_seconds,
    logger,
    *args,
    **kwargs
):
    """
    Execute an operation with configurable retry handling.

    Args:
        operation: Function to execute.
        max_retries: Maximum number of attempts.
        retry_delay_seconds: Delay between attempts.
        logger: Logger used to record retry activity.
        *args: Positional arguments passed to the operation.
        **kwargs: Keyword arguments passed to the operation.

    Returns:
        Result returned by the operation.
    """

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                "Executing %s - attempt %s/%s",
                operation.__name__,
                attempt,
                max_retries
            )

            result = operation(
                *args,
                **kwargs
            )

            logger.info(
                "%s completed successfully.",
                operation.__name__
            )

            return result

        except Exception as error:
            logger.error(
                "%s failed on attempt %s/%s: %s",
                operation.__name__,
                attempt,
                max_retries,
                error
            )

            if attempt == max_retries:
                logger.exception(
                    "%s failed after %s attempts.",
                    operation.__name__,
                    max_retries
                )
                raise

            logger.warning(
                "Retrying in %s seconds...",
                retry_delay_seconds
            )

            time.sleep(retry_delay_seconds)
