import json
from pathlib import Path


DEFAULT_CONFIG_PATH = Path("config/pipeline_config.json")


def load_config(config_path=DEFAULT_CONFIG_PATH):
    """
    Load and validate pipeline configuration from JSON.

    Args:
        config_path: Path to the pipeline configuration file.

    Returns:
        dict: Parsed pipeline configuration.
    """

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with open(
        config_path,
        mode="r",
        encoding="utf-8"
    ) as config_file:
        config = json.load(config_file)

    required_sections = [
        "pipeline",
        "source",
        "target",
        "data_quality",
        "monitoring"
    ]

    missing_sections = [
        section
        for section in required_sections
        if section not in config
    ]

    if missing_sections:
        raise ValueError(
            "Missing required configuration sections: "
            + ", ".join(missing_sections)
        )

    return config


if __name__ == "__main__":
    pipeline_config = load_config()

    print("Configuration loaded successfully.")
    print(
        "Pipeline:",
        pipeline_config["pipeline"]["name"]
    )
    print(
        "Environment:",
        pipeline_config["pipeline"]["environment"]
    )
