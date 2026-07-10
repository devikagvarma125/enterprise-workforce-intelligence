from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
SQL_DIR = PROJECT_ROOT / "sql"
DB_PATH = SQL_DIR / "workforce_intelligence.db"


GOLD_TABLES = [
    "dim_employee",
    "dim_department",
    "dim_job_role",
    "dim_location",
    "dim_date",
    "dim_manager",
    "dim_security_user",
    "fact_payroll",
    "fact_attendance",
    "fact_leave",
    "fact_recruitment",
    "fact_training",
    "fact_performance",
    "fact_attrition",
    "ml_attrition_dataset",
    "gold_build_summary",
    "gold_relationship_validation",
]


INDEX_SCRIPT = """
CREATE INDEX IF NOT EXISTS idx_dim_employee_employee_key
ON dim_employee(employee_key);

CREATE INDEX IF NOT EXISTS idx_dim_employee_department_key
ON dim_employee(department_key);

CREATE INDEX IF NOT EXISTS idx_dim_employee_location_key
ON dim_employee(location_key);

CREATE INDEX IF NOT EXISTS idx_fact_payroll_employee_key
ON fact_payroll(employee_key);

CREATE INDEX IF NOT EXISTS idx_fact_attendance_employee_key
ON fact_attendance(employee_key);

CREATE INDEX IF NOT EXISTS idx_fact_leave_employee_key
ON fact_leave(employee_key);

CREATE INDEX IF NOT EXISTS idx_fact_training_employee_key
ON fact_training(employee_key);

CREATE INDEX IF NOT EXISTS idx_fact_performance_employee_key
ON fact_performance(employee_key);

CREATE INDEX IF NOT EXISTS idx_fact_attrition_employee_key
ON fact_attrition(employee_key);

CREATE INDEX IF NOT EXISTS idx_dim_date_date_key
ON dim_date(date_key);
"""


def load_gold_table_to_sqlite(connection: sqlite3.Connection, table_name: str) -> dict:
    file_path = GOLD_DIR / f"{table_name}.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Gold file not found: {file_path}")

    dataframe = pd.read_csv(file_path)

    dataframe.to_sql(
        name=table_name,
        con=connection,
        if_exists="replace",
        index=False,
    )

    return {
        "table_name": table_name,
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
    }


def main() -> None:
    print("Loading Gold CSV tables into local SQLite database...")

    SQL_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)

    try:
        load_summary = []

        for table_name in GOLD_TABLES:
            result = load_gold_table_to_sqlite(connection, table_name)
            load_summary.append(result)
            print(
                f"Loaded {table_name}: "
                f"{result['row_count']:,} rows, "
                f"{result['column_count']} columns"
            )

        connection.executescript(INDEX_SCRIPT)
        connection.commit()

        summary_df = pd.DataFrame(load_summary)
        summary_path = SQL_DIR / "sqlite_load_summary.csv"
        summary_df.to_csv(summary_path, index=False)

        print("\nSQLite database created successfully.")
        print(f"Database path: {DB_PATH}")
        print(f"Load summary: {summary_path}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()