from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"

SOURCE_SYSTEM = "Synthetic HR Source"


RAW_FILES = {
    "employees": "employees.csv",
    "payroll": "payroll.csv",
    "attendance": "attendance.csv",
    "leave": "leave.csv",
    "recruitment": "recruitment.csv",
    "training": "training.csv",
    "performance": "performance.csv",
    "attrition": "attrition.csv",
    "security_mapping": "security_mapping.csv",
}


def standardise_column_name(column_name: str) -> str:
    """
    Convert column names into a consistent snake_case format.

    Example:
        Employee ID -> employee_id
        Hire-Date   -> hire_date
    """
    column_name = column_name.strip().lower()
    column_name = re.sub(r"[^a-z0-9]+", "_", column_name)
    column_name = re.sub(r"_+", "_", column_name)
    return column_name.strip("_")


def load_raw_file(file_path: Path) -> pd.DataFrame:
    """
    Load a raw CSV file.

    We read values as strings at the Bronze stage to preserve source data
    before applying business rules in the Silver layer.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Raw source file not found: {file_path}")

    return pd.read_csv(file_path, dtype=str)


def create_bronze_table(dataset_name: str, file_name: str, pipeline_run_id: str) -> dict:
    """
    Read one raw source file and create one Bronze output file.
    """
    raw_file_path = RAW_DIR / file_name
    bronze_file_path = BRONZE_DIR / f"bronze_{dataset_name}.csv"

    df = load_raw_file(raw_file_path)

    original_row_count = len(df)
    original_column_count = len(df.columns)

    df.columns = [standardise_column_name(col) for col in df.columns]

    ingestion_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    df["ingestion_timestamp"] = ingestion_timestamp
    df["source_file_name"] = file_name
    df["source_system"] = SOURCE_SYSTEM
    df["pipeline_run_id"] = pipeline_run_id

    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(bronze_file_path, index=False)

    return {
        "dataset_name": dataset_name,
        "source_file": str(raw_file_path.relative_to(PROJECT_ROOT)),
        "bronze_file": str(bronze_file_path.relative_to(PROJECT_ROOT)),
        "source_rows": original_row_count,
        "bronze_rows": len(df),
        "source_columns": original_column_count,
        "bronze_columns": len(df.columns),
        "status": "Success",
    }


def run_raw_to_bronze() -> None:
    """
    Run Raw to Bronze ingestion for all HR source files.
    """
    print("Starting Raw to Bronze ingestion...")

    pipeline_run_id = f"RUN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    ingestion_results = []

    for dataset_name, file_name in RAW_FILES.items():
        result = create_bronze_table(dataset_name, file_name, pipeline_run_id)
        ingestion_results.append(result)
        print(
            f"Created {result['bronze_file']} "
            f"({result['bronze_rows']} rows)"
        )

    summary_df = pd.DataFrame(ingestion_results)
    summary_file_path = BRONZE_DIR / "bronze_ingestion_summary.csv"
    summary_df.to_csv(summary_file_path, index=False)

    print("\nRaw to Bronze ingestion completed successfully.")
    print(f"Pipeline Run ID: {pipeline_run_id}")
    print(f"Ingestion summary created at: {summary_file_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    run_raw_to_bronze()