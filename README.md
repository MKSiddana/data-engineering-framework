# Data Engineering Framework

A reusable, configuration-driven Python framework for building reliable data pipelines with centralized logging, data-quality validation, retry handling, audit metrics, and database loading.

This project demonstrates production-oriented data engineering patterns that can be reused across multiple ETL and ELT pipelines.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │ Pipeline Config JSON│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Configuration Loader│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    CSV Extractor    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Quality Engine │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Retry / Error Logic │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SQLite Loader    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Audit + Monitoring  │
                    └─────────────────────┘

          Centralized logging operates across all stages
```

---

## Key Features

- Configuration-driven pipeline execution
- Reusable CSV extraction component
- Configurable data-quality validation
- Required-column validation
- Null-value detection
- Duplicate business-key detection
- Reusable SQLite loading
- Idempotent upsert behavior
- Configurable retry handling
- Centralized console and file logging
- Pipeline run IDs
- Success and failure auditing
- Source, processed, and rejected record metrics
- Pipeline execution duration tracking
- Unit testing for data-quality components

---

## Project Structure

```text
data-engineering-framework/
│
├── config/
│   └── pipeline_config.json
│
├── data/
│   └── sample_customers.csv
│
├── framework/
│   ├── __init__.py
│   ├── audit.py
│   ├── config_loader.py
│   ├── data_quality.py
│   ├── extractor.py
│   ├── loader.py
│   ├── logger.py
│   └── retry.py
│
├── tests/
│   └── test_data_quality.py
│
├── .gitignore
├── pipeline.py
└── README.md
```

---

## Configuration-Driven Design

Pipeline behavior is controlled through:

```text
config/pipeline_config.json
```

The configuration defines:

- Pipeline name and environment
- Retry settings
- Source type and location
- Target database and table
- Required columns
- Unique business keys
- Null-handling rules
- Logging and audit settings

This approach separates pipeline logic from environment-specific configuration.

---

## Data Quality

The reusable data-quality engine validates incoming datasets using rules defined in configuration.

Current checks include:

- Required columns
- Null or empty values
- Duplicate business keys

Additional rules can be added without redesigning the pipeline orchestration layer.

---

## Reliability and Error Handling

Pipeline operations can use configurable retry behavior.

Failed operations are logged and retried according to:

```text
max_retries
retry_delay_seconds
```

After the configured number of attempts is exhausted, the exception is raised and the pipeline run is recorded as failed.

---

## Audit and Monitoring

Every pipeline execution generates audit information including:

- Unique run ID
- Pipeline name
- Start time
- End time
- Execution duration
- Source record count
- Processed record count
- Rejected record count
- Pipeline status
- Error message

Runtime audit files and logs are written under the local `output/` directory and excluded from source control.

---

## Local Execution

From the repository root:

```bash
python pipeline.py
```

Run unit tests with:

```bash
python -m unittest discover tests
```

The pipeline uses Python's standard library and SQLite, so no external database infrastructure is required for the local demonstration.

---

## Example Pipeline Flow

```text
Configuration
      ↓
Extract CSV
      ↓
Data Quality Validation
      ↓
Retry-Controlled Load
      ↓
SQLite Target
      ↓
Audit Metrics + Logs
```

---

## Production Extension

The framework is intentionally modular so the local components can be extended for enterprise environments.

Potential extensions include:

- Azure Data Factory orchestration
- Azure Data Lake Storage Gen2
- Azure SQL Database
- Databricks and PySpark processing
- Snowflake targets
- REST API ingestion
- Cloud-based configuration management
- Azure Key Vault integration
- Email or Microsoft Teams alerts
- CI/CD with GitHub Actions
- Centralized monitoring dashboards
- Additional data-quality rule types

These integrations are architectural extension points and are not part of the current local executable implementation.

---

## Data Privacy

All customer records included in this repository are synthetic and created solely for demonstration purposes.

The project contains no proprietary employer data, client data, production credentials, or confidential source code.

---

## Author

**Madhuri Krishna Siddana**

Senior Data Engineer focused on scalable ETL/ELT pipelines, cloud data platforms, distributed processing, data quality, monitoring, and reliable production data systems.
