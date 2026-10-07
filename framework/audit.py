import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


AUDIT_DIRECTORY = Path("output/audit")


def start_pipeline_audit(pipeline_name):
    """
    Create audit information for a new pipeline run.
    """
    return {
        "run_id": str(uuid.uuid4()),
        "pipeline_name": pipeline_name,
        "status": "STARTED",
        "start_time": datetime.now(timezone.utc),
        "end_time": None,
        "duration_seconds": None,
        "source_record_count": 0,
        "processed_record_count": 0,
        "rejected_record_count": 0,
        "error_message": None
    }


def complete_pipeline_audit(
    audit,
    status,
    source_count=0,
    processed_count=0,
    rejected_count=0,
    error_message=None
):
    """
    Complete pipeline audit information and
    persist the result as JSON.
    """
    end_time = datetime.now(timezone.utc)

    audit["status"] = status
    audit["end_time"] = end_time
    audit["duration_seconds"] = round(
        (end_time - audit["start_time"]).total_seconds(),
        3
    )
    audit["source_record_count"] = source_count
    audit["processed_record_count"] = processed_count
    audit["rejected_record_count"] = rejected_count
    audit["error_message"] = error_message

    AUDIT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    audit_file = (
        AUDIT_DIRECTORY
        / f"{audit['run_id']}.json"
    )

    serializable_audit = audit.copy()
    serializable_audit["start_time"] = (
        audit["start_time"].isoformat()
    )
    serializable_audit["end_time"] = (
        audit["end_time"].isoformat()
    )

    with open(
        audit_file,
        mode="w",
        encoding="utf-8"
    ) as file:
        json.dump(
            serializable_audit,
            file,
            indent=4
        )

    return serializable_audit
