from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"
DB_PATH = SQL_DIR / "workforce_intelligence.db"
QUERY_RESULTS_DIR = SQL_DIR / "query_results"


SQL_FILES = [
    SQL_DIR / "01_workforce_analytics_queries.sql",
    SQL_DIR / "02_data_quality_checks.sql",
]


def parse_named_queries(sql_text: str) -> dict[str, str]:
    """
    Parse SQL queries marked using:

    -- name: query_name
    SELECT ...
    ;
    """
    queries: dict[str, str] = {}
    current_name: str | None = None
    current_lines: list[str] = []

    for line in sql_text.splitlines():
        match = re.match(r"^\s*--\s*name:\s*(.+?)\s*$", line, flags=re.IGNORECASE)

        if match:
            if current_name and current_lines:
                query = "\n".join(current_lines).strip().rstrip(";")
                if query:
                    queries[current_name] = query

            current_name = match.group(1).strip()
            current_lines = []
        elif current_name:
            current_lines.append(line)

    if current_name and current_lines:
        query = "\n".join(current_lines).strip().rstrip(";")
        if query:
            queries[current_name] = query

    return queries


def run_sql_file(connection: sqlite3.Connection, sql_file: Path) -> None:
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    sql_text = sql_file.read_text(encoding="utf-8")
    queries = parse_named_queries(sql_text)

    if not queries:
        print(f"No named queries found in {sql_file.name}")
        return

    for query_name, query in queries.items():
        dataframe = pd.read_sql_query(query, connection)

        output_file_name = f"{sql_file.stem}_{query_name}.csv"
        output_path = QUERY_RESULTS_DIR / output_file_name

        dataframe.to_csv(output_path, index=False)

        print(
            f"Executed {query_name}: "
            f"{len(dataframe):,} rows -> {output_path.relative_to(PROJECT_ROOT)}"
        )


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DB_PATH}. "
            "Run scripts/load_gold_to_sqlite.py first."
        )

    QUERY_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        for sql_file in SQL_FILES:
            print(f"\nRunning SQL file: {sql_file.name}")
            run_sql_file(connection, sql_file)

        print("\nSQL query execution completed successfully.")
        print(f"Query results folder: {QUERY_RESULTS_DIR}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()