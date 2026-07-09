from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"

REFERENCE_DATE = pd.Timestamp("2026-06-30")


SILVER_FILES = {
    "employees": "silver_employees.csv",
    "payroll": "silver_payroll.csv",
    "attendance": "silver_attendance.csv",
    "leave": "silver_leave.csv",
    "recruitment": "silver_recruitment.csv",
    "training": "silver_training.csv",
    "performance": "silver_performance.csv",
    "attrition": "silver_attrition.csv",
    "security_mapping": "silver_security_mapping.csv",
}


DEPARTMENT_GROUP = {
    "HR": "People",
    "Finance": "Finance",
    "Sales": "Commercial",
    "Marketing": "Commercial",
    "IT": "Technology",
    "Operations": "Operations",
    "Customer Support": "Customer Operations",
    "Legal": "Corporate",
}


JOB_FAMILY_BY_DEPARTMENT = {
    "HR": "People",
    "Finance": "Finance",
    "Sales": "Commercial",
    "Marketing": "Commercial",
    "IT": "Technology",
    "Operations": "Operations",
    "Customer Support": "Customer Operations",
    "Legal": "Corporate",
}


LOCATION_REGION = {
    "London": "London and South East",
    "Manchester": "North West",
    "Birmingham": "West Midlands",
    "Leeds": "Yorkshire and Humber",
    "Bristol": "South West",
    "Edinburgh": "Scotland",
}


SALARY_BAND_SORT = {
    "Under 30K": 1,
    "30K-40K": 2,
    "40K-50K": 3,
    "50K-65K": 4,
    "65K-80K": 5,
    "80K-100K": 6,
    "100K+": 7,
}


def read_silver_table(dataset_name: str) -> pd.DataFrame:
    """Read one Silver CSV table."""
    file_name = SILVER_FILES[dataset_name]
    path = SILVER_DIR / file_name

    if not path.exists():
        raise FileNotFoundError(f"Silver file not found: {path}")

    return pd.read_csv(path, dtype=str)


def normalise_blank_values(df: pd.DataFrame) -> pd.DataFrame:
    """Trim text values and convert blank-like strings to missing values."""
    output = df.copy()

    for column in output.columns:
        output[column] = output[column].astype("string").str.strip()
        output[column] = output[column].replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "NaN": pd.NA,
                "None": pd.NA,
                "NaT": pd.NA,
                "<NA>": pd.NA,
            }
        )

    return output


def parse_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to datetime values."""
    output = df.copy()

    for column in columns:
        if column in output.columns:
            output[column] = pd.to_datetime(output[column], errors="coerce")

    return output


def parse_numbers(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to numeric values."""
    output = df.copy()

    for column in columns:
        if column in output.columns:
            output[column] = pd.to_numeric(output[column], errors="coerce")

    return output


def date_key(series: pd.Series) -> pd.Series:
    """Convert a date series into YYYYMMDD nullable integer keys."""
    date_series = pd.to_datetime(series, errors="coerce")
    return pd.to_numeric(date_series.dt.strftime("%Y%m%d"), errors="coerce").astype(
        "Int64"
    )


def add_surrogate_key(df: pd.DataFrame, key_name: str) -> pd.DataFrame:
    """Add a 1-based surrogate key column as the first column."""
    output = df.reset_index(drop=True).copy()
    output.insert(0, key_name, range(1, len(output) + 1))
    return output


def write_gold_table(df: pd.DataFrame, table_name: str) -> None:
    """Write a Gold dataframe to CSV."""
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    output = df.copy()

    for column in output.columns:
        if pd.api.types.is_datetime64_any_dtype(output[column]):
            output[column] = output[column].dt.strftime("%Y-%m-%d")

    output.to_csv(GOLD_DIR / f"{table_name}.csv", index=False)


def clean_source_tables() -> dict[str, pd.DataFrame]:
    """Read Silver tables and apply Gold-stage type conversions."""
    employees = normalise_blank_values(read_silver_table("employees"))
    payroll = normalise_blank_values(read_silver_table("payroll"))
    attendance = normalise_blank_values(read_silver_table("attendance"))
    leave_df = normalise_blank_values(read_silver_table("leave"))
    recruitment = normalise_blank_values(read_silver_table("recruitment"))
    training = normalise_blank_values(read_silver_table("training"))
    performance = normalise_blank_values(read_silver_table("performance"))
    attrition = normalise_blank_values(read_silver_table("attrition"))
    security = normalise_blank_values(read_silver_table("security_mapping"))

    employees = parse_dates(employees, ["date_of_birth", "hire_date", "exit_date"])
    employees = parse_numbers(employees, ["age", "tenure_years"])

    payroll = parse_dates(payroll, ["pay_period"])
    payroll = parse_numbers(
        payroll,
        [
            "annual_salary",
            "monthly_salary",
            "bonus_amount",
            "salary_band_sort_order",
        ],
    )

    attendance = parse_dates(attendance, ["attendance_month"])
    attendance = parse_numbers(
        attendance,
        [
            "working_days",
            "present_days",
            "absent_days",
            "late_arrivals",
            "remote_work_days",
            "overtime_hours",
            "attendance_rate",
            "absence_rate",
        ],
    )

    leave_df = parse_dates(leave_df, ["leave_start_date", "leave_end_date"])
    leave_df = parse_numbers(leave_df, ["leave_days", "leave_year"])

    recruitment = parse_dates(
        recruitment,
        ["application_date", "interview_date", "offer_date", "hire_date"],
    )
    recruitment = parse_numbers(recruitment, ["time_to_hire_days"])

    training = parse_dates(training, ["assigned_date", "completion_date"])
    training = parse_numbers(
        training,
        ["completion_flag", "training_hours", "training_score"],
    )

    performance = parse_numbers(
        performance,
        [
            "review_year",
            "performance_rating",
            "potential_rating",
            "promotion_flag",
        ],
    )

    attrition = parse_dates(attrition, ["exit_date"])
    attrition = parse_numbers(
        attrition,
        ["attrition_flag", "regrettable_attrition_flag", "notice_period_days"],
    )

    security["user_email"] = security["user_email"].str.lower()
    security["access_type"] = security["access_type"].str.upper()

    return {
        "employees": employees,
        "payroll": payroll,
        "attendance": attendance,
        "leave": leave_df,
        "recruitment": recruitment,
        "training": training,
        "performance": performance,
        "attrition": attrition,
        "security_mapping": security,
    }


def enrich_employee_fields(employees: pd.DataFrame) -> pd.DataFrame:
    """Ensure employee derived fields exist before building dimensions."""
    output = employees.copy()

    if "full_name" not in output.columns:
        output["full_name"] = (
            output["first_name"].fillna("").astype(str).str.strip()
            + " "
            + output["last_name"].fillna("").astype(str).str.strip()
        ).str.strip()

    if "exit_date" not in output.columns:
        output["exit_date"] = pd.NaT

    if "age" not in output.columns or output["age"].isna().all():
        output["age"] = np.floor(
            (REFERENCE_DATE - output["date_of_birth"]).dt.days / 365.25
        )

    if "tenure_years" not in output.columns or output["tenure_years"].isna().all():
        tenure_end = output["exit_date"].fillna(REFERENCE_DATE)
        output["tenure_years"] = ((tenure_end - output["hire_date"]).dt.days / 365.25).round(2)

    return output


def create_dim_department(employees: pd.DataFrame, recruitment: pd.DataFrame) -> pd.DataFrame:
    departments = pd.concat(
        [
            employees[["department"]],
            recruitment[["department"]] if "department" in recruitment.columns else pd.DataFrame(columns=["department"]),
        ],
        ignore_index=True,
    )

    departments = departments.dropna().drop_duplicates().sort_values("department")
    departments = departments.rename(columns={"department": "department_name"})
    departments["department_group"] = departments["department_name"].map(DEPARTMENT_GROUP).fillna("Other")

    return add_surrogate_key(departments, "department_key")


def create_dim_job_role(employees: pd.DataFrame, recruitment: pd.DataFrame) -> pd.DataFrame:
    employee_roles = employees[["job_role", "job_level", "department"]].dropna(subset=["job_role"]).copy()

    if "job_role" in recruitment.columns:
        recruitment_roles = recruitment[["job_role", "department"]].dropna(subset=["job_role"]).copy()
        recruitment_roles = recruitment_roles.merge(
            employee_roles[["job_role", "job_level"]].drop_duplicates("job_role"),
            on="job_role",
            how="left",
        )
        roles = pd.concat([employee_roles, recruitment_roles], ignore_index=True)
    else:
        roles = employee_roles

    roles["job_level"] = roles["job_level"].fillna("Unknown")
    roles["job_family"] = roles["department"].map(JOB_FAMILY_BY_DEPARTMENT).fillna("Other")

    roles = roles[["job_role", "job_level", "job_family"]]
    roles = roles.drop_duplicates().sort_values(["job_family", "job_level", "job_role"])

    return add_surrogate_key(roles, "job_role_key")


def create_dim_location(employees: pd.DataFrame, recruitment: pd.DataFrame) -> pd.DataFrame:
    locations = pd.concat(
        [
            employees[["location", "country"]],
            recruitment[["location"]].assign(country="United Kingdom")
            if "location" in recruitment.columns
            else pd.DataFrame(columns=["location", "country"]),
        ],
        ignore_index=True,
    )

    locations = locations.dropna(subset=["location"]).drop_duplicates("location")
    locations["country"] = locations["country"].fillna("United Kingdom")
    locations["region"] = locations["location"].map(LOCATION_REGION).fillna("Other")
    locations = locations[["location", "country", "region"]].sort_values("location")

    return add_surrogate_key(locations, "location_key")


def create_dim_manager(employees: pd.DataFrame) -> pd.DataFrame:
    manager_ids = set(employees["manager_id"].dropna().astype(str))
    manager_ids.discard("")

    managers = employees[employees["employee_id"].isin(manager_ids)].copy()

    manager_dim = managers[["employee_id", "full_name", "department"]].rename(
        columns={
            "employee_id": "manager_id",
            "full_name": "manager_name",
            "department": "manager_department",
        }
    )

    missing_manager_ids = sorted(manager_ids - set(manager_dim["manager_id"].astype(str)))

    if missing_manager_ids:
        missing_rows = pd.DataFrame(
            {
                "manager_id": missing_manager_ids,
                "manager_name": "Unknown Manager",
                "manager_department": "Unknown",
            }
        )
        manager_dim = pd.concat([manager_dim, missing_rows], ignore_index=True)

    manager_dim = manager_dim.drop_duplicates("manager_id").sort_values("manager_id")

    return add_surrogate_key(manager_dim, "manager_key")


def create_dim_security_user(security: pd.DataFrame) -> pd.DataFrame:
    security_dim = security[
        [
            "user_email",
            "user_name",
            "access_type",
            "department",
            "location",
            "role_description",
        ]
    ].copy()

    security_dim = security_dim.dropna(subset=["user_email"])
    security_dim = security_dim.drop_duplicates(
        subset=["user_email", "access_type", "department", "location"]
    )
    security_dim = security_dim.sort_values(["access_type", "user_email"])

    return add_surrogate_key(security_dim, "security_user_key")


def create_dim_employee(
    employees: pd.DataFrame,
    dim_department: pd.DataFrame,
    dim_job_role: pd.DataFrame,
    dim_location: pd.DataFrame,
    dim_manager: pd.DataFrame,
) -> pd.DataFrame:
    employee_dim = employees.copy()

    department_map = dict(zip(dim_department["department_name"], dim_department["department_key"]))
    location_map = dict(zip(dim_location["location"], dim_location["location_key"]))
    manager_map = dict(zip(dim_manager["manager_id"], dim_manager["manager_key"]))

    role_map = dict(zip(dim_job_role["job_role"], dim_job_role["job_role_key"]))

    employee_dim["department_key"] = employee_dim["department"].map(department_map).astype("Int64")
    employee_dim["job_role_key"] = employee_dim["job_role"].map(role_map).astype("Int64")
    employee_dim["location_key"] = employee_dim["location"].map(location_map).astype("Int64")
    employee_dim["manager_key"] = employee_dim["manager_id"].map(manager_map).astype("Int64")

    target_columns = [
        "employee_id",
        "full_name",
        "gender",
        "date_of_birth",
        "age",
        "hire_date",
        "exit_date",
        "tenure_years",
        "employee_status",
        "employment_type",
        "work_mode",
        "department_key",
        "job_role_key",
        "location_key",
        "manager_key",
        "email",
    ]

    employee_dim = employee_dim[target_columns].drop_duplicates("employee_id")
    employee_dim = employee_dim.sort_values("employee_id")

    return add_surrogate_key(employee_dim, "employee_key")


def create_dim_date(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    date_columns = {
        "employees": ["date_of_birth", "hire_date", "exit_date"],
        "payroll": ["pay_period"],
        "attendance": ["attendance_month"],
        "leave": ["leave_start_date", "leave_end_date"],
        "recruitment": ["application_date", "interview_date", "offer_date", "hire_date"],
        "training": ["assigned_date", "completion_date"],
        "attrition": ["exit_date"],
    }

    all_dates: list[pd.Series] = []

    for table_name, columns in date_columns.items():
        table = tables.get(table_name)
        if table is None:
            continue
        for column in columns:
            if column in table.columns:
                parsed_dates = pd.to_datetime(table[column], errors="coerce").dropna()
                if not parsed_dates.empty:
                    all_dates.append(parsed_dates)

    if all_dates:
        combined_dates = pd.concat(all_dates, ignore_index=True)
        start_date = combined_dates.min().normalize()
        end_date = combined_dates.max().normalize()
    else:
        start_date = pd.Timestamp("2024-01-01")
        end_date = REFERENCE_DATE

    calendar = pd.DataFrame({"full_date": pd.date_range(start_date, end_date, freq="D")})
    calendar["date_key"] = date_key(calendar["full_date"])
    calendar["day"] = calendar["full_date"].dt.day
    calendar["month"] = calendar["full_date"].dt.month
    calendar["month_name"] = calendar["full_date"].dt.month_name()
    calendar["quarter"] = "Q" + calendar["full_date"].dt.quarter.astype(str)
    calendar["year"] = calendar["full_date"].dt.year
    calendar["week_of_year"] = calendar["full_date"].dt.isocalendar().week.astype("Int64")
    calendar["is_weekend"] = np.where(calendar["full_date"].dt.dayofweek >= 5, 1, 0)

    calendar = calendar[
        [
            "date_key",
            "full_date",
            "day",
            "month",
            "month_name",
            "quarter",
            "year",
            "week_of_year",
            "is_weekend",
        ]
    ]

    return calendar


def create_lookup_maps(
    dim_employee: pd.DataFrame,
    dim_department: pd.DataFrame,
    dim_job_role: pd.DataFrame,
    dim_location: pd.DataFrame,
    dim_manager: pd.DataFrame,
) -> dict[str, dict]:
    return {
        "employee": dict(zip(dim_employee["employee_id"], dim_employee["employee_key"])),
        "department": dict(zip(dim_department["department_name"], dim_department["department_key"])),
        "job_role": dict(zip(dim_job_role["job_role"], dim_job_role["job_role_key"])),
        "location": dict(zip(dim_location["location"], dim_location["location_key"])),
        "manager": dict(zip(dim_manager["manager_id"], dim_manager["manager_key"])),
    }


def create_fact_payroll(payroll: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = payroll.copy()
    fact["employee_key"] = fact["employee_id"].map(lookups["employee"]).astype("Int64")
    fact["pay_period_key"] = date_key(fact["pay_period"])

    fact["salary_band_sort_order"] = fact["salary_band_sort_order"].fillna(
        fact["salary_band"].map(SALARY_BAND_SORT)
    )

    fact = fact[
        [
            "payroll_id",
            "employee_key",
            "pay_period_key",
            "annual_salary",
            "monthly_salary",
            "bonus_amount",
            "pay_grade",
            "salary_band",
            "salary_band_sort_order",
            "currency",
        ]
    ].sort_values(["employee_key", "pay_period_key", "payroll_id"])

    return add_surrogate_key(fact, "payroll_key")


def create_fact_attendance(attendance: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = attendance.copy()
    fact["employee_key"] = fact["employee_id"].map(lookups["employee"]).astype("Int64")
    fact["attendance_month_key"] = date_key(fact["attendance_month"])

    fact = fact[
        [
            "attendance_id",
            "employee_key",
            "attendance_month_key",
            "working_days",
            "present_days",
            "absent_days",
            "late_arrivals",
            "remote_work_days",
            "overtime_hours",
            "attendance_rate",
            "absence_rate",
        ]
    ].sort_values(["employee_key", "attendance_month_key", "attendance_id"])

    return add_surrogate_key(fact, "attendance_key")


def create_fact_leave(leave_df: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = leave_df.copy()
    fact["employee_key"] = fact["employee_id"].map(lookups["employee"]).astype("Int64")
    fact["leave_start_date_key"] = date_key(fact["leave_start_date"])
    fact["leave_end_date_key"] = date_key(fact["leave_end_date"])

    fact = fact[
        [
            "leave_id",
            "employee_key",
            "leave_start_date_key",
            "leave_end_date_key",
            "leave_type",
            "leave_days",
            "leave_status",
            "leave_year",
        ]
    ].sort_values(["employee_key", "leave_start_date_key", "leave_id"])

    return add_surrogate_key(fact, "leave_key")


def create_fact_recruitment(recruitment: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = recruitment.copy()

    fact["department_key"] = fact["department"].map(lookups["department"]).astype("Int64")
    fact["job_role_key"] = fact["job_role"].map(lookups["job_role"]).astype("Int64")
    fact["location_key"] = fact["location"].map(lookups["location"]).astype("Int64")
    fact["hired_employee_key"] = fact["hired_employee_id"].map(lookups["employee"]).astype("Int64")

    fact["application_date_key"] = date_key(fact["application_date"])
    fact["interview_date_key"] = date_key(fact["interview_date"])
    fact["offer_date_key"] = date_key(fact["offer_date"])
    fact["hire_date_key"] = date_key(fact["hire_date"])

    fact = fact[
        [
            "candidate_id",
            "requisition_id",
            "department_key",
            "job_role_key",
            "location_key",
            "application_date_key",
            "interview_date_key",
            "offer_date_key",
            "hire_date_key",
            "recruitment_source",
            "status",
            "hired_employee_key",
            "time_to_hire_days",
        ]
    ].sort_values(["application_date_key", "candidate_id"])

    return add_surrogate_key(fact, "recruitment_key")


def create_fact_training(training: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = training.copy()
    fact["employee_key"] = fact["employee_id"].map(lookups["employee"]).astype("Int64")
    fact["assigned_date_key"] = date_key(fact["assigned_date"])
    fact["completion_date_key"] = date_key(fact["completion_date"])

    fact = fact[
        [
            "training_id",
            "employee_key",
            "assigned_date_key",
            "completion_date_key",
            "course_name",
            "course_category",
            "completion_status",
            "completion_flag",
            "training_hours",
            "training_score",
        ]
    ].sort_values(["employee_key", "assigned_date_key", "training_id"])

    return add_surrogate_key(fact, "training_key")


def create_fact_performance(performance: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = performance.copy()
    fact["employee_key"] = fact["employee_id"].map(lookups["employee"]).astype("Int64")
    fact["manager_key"] = fact["manager_id"].map(lookups["manager"]).astype("Int64")

    fact = fact[
        [
            "performance_id",
            "employee_key",
            "review_year",
            "review_period",
            "performance_rating",
            "potential_rating",
            "promotion_flag",
            "manager_key",
        ]
    ].sort_values(["employee_key", "review_year", "review_period", "performance_id"])

    return add_surrogate_key(fact, "performance_key")


def create_fact_attrition(attrition: pd.DataFrame, lookups: dict[str, dict]) -> pd.DataFrame:
    fact = attrition.copy()
    fact["employee_key"] = fact["employee_id"].map(lookups["employee"]).astype("Int64")
    fact["exit_date_key"] = date_key(fact["exit_date"])
    fact["attrition_flag"] = fact["attrition_flag"].fillna(1).astype("Int64")

    fact = fact[
        [
            "attrition_id",
            "employee_key",
            "exit_date_key",
            "exit_reason",
            "attrition_type",
            "attrition_flag",
            "regrettable_attrition_flag",
            "notice_period_days",
        ]
    ].sort_values(["employee_key", "exit_date_key", "attrition_id"])

    return add_surrogate_key(fact, "attrition_key")


def latest_record_by_employee(
    fact: pd.DataFrame,
    sort_columns: list[str],
    selected_columns: list[str],
) -> pd.DataFrame:
    """Return latest record per employee_key using supplied sorting columns."""
    if fact.empty:
        return pd.DataFrame(columns=["employee_key", *selected_columns])

    sorted_fact = fact.sort_values(["employee_key", *sort_columns])
    latest = sorted_fact.groupby("employee_key", as_index=False).tail(1)
    return latest[["employee_key", *selected_columns]]


def create_ml_attrition_dataset(
    dim_employee: pd.DataFrame,
    dim_department: pd.DataFrame,
    dim_job_role: pd.DataFrame,
    dim_location: pd.DataFrame,
    fact_payroll: pd.DataFrame,
    fact_attendance: pd.DataFrame,
    fact_training: pd.DataFrame,
    fact_performance: pd.DataFrame,
    fact_attrition: pd.DataFrame,
) -> pd.DataFrame:
    """Create one modelling row per employee for attrition prediction."""
    employee_features = dim_employee[
        [
            "employee_key",
            "employee_id",
            "age",
            "gender",
            "department_key",
            "job_role_key",
            "location_key",
            "work_mode",
            "tenure_years",
        ]
    ].copy()

    employee_features = employee_features.merge(
        dim_department[["department_key", "department_name"]],
        on="department_key",
        how="left",
    )
    employee_features = employee_features.merge(
        dim_job_role[["job_role_key", "job_role", "job_level"]],
        on="job_role_key",
        how="left",
    )
    employee_features = employee_features.merge(
        dim_location[["location_key", "location"]],
        on="location_key",
        how="left",
    )

    latest_payroll = latest_record_by_employee(
        fact_payroll,
        ["pay_period_key"],
        ["annual_salary", "salary_band"],
    )

    attendance_features = (
        fact_attendance.groupby("employee_key", as_index=False)
        .agg(
            absence_rate=("absence_rate", "mean"),
            attendance_rate=("attendance_rate", "mean"),
            late_arrivals=("late_arrivals", "sum"),
            overtime_hours=("overtime_hours", "sum"),
        )
        .round(4)
    )

    training_features = (
        fact_training.groupby("employee_key", as_index=False)
        .agg(
            training_hours=("training_hours", "sum"),
            training_completion_rate=("completion_flag", "mean"),
        )
        .round(4)
    )
    training_features["training_completion_flag"] = np.where(
        training_features["training_completion_rate"].fillna(0) >= 0.5,
        1,
        0,
    )

    performance_latest = latest_record_by_employee(
        fact_performance,
        ["review_year", "performance_key"],
        ["performance_rating", "potential_rating", "promotion_flag"],
    )

    attrition_flags = fact_attrition[["employee_key", "attrition_flag"]].drop_duplicates(
        "employee_key"
    )

    ml = employee_features.merge(latest_payroll, on="employee_key", how="left")
    ml = ml.merge(attendance_features, on="employee_key", how="left")
    ml = ml.merge(training_features, on="employee_key", how="left")
    ml = ml.merge(performance_latest, on="employee_key", how="left")
    ml = ml.merge(attrition_flags, on="employee_key", how="left")

    ml["attrition_flag"] = ml["attrition_flag"].fillna(0).astype("Int64")
    ml["absence_rate"] = ml["absence_rate"].fillna(0)
    ml["attendance_rate"] = ml["attendance_rate"].fillna(0)
    ml["late_arrivals"] = ml["late_arrivals"].fillna(0)
    ml["overtime_hours"] = ml["overtime_hours"].fillna(0)
    ml["training_hours"] = ml["training_hours"].fillna(0)
    ml["training_completion_rate"] = ml["training_completion_rate"].fillna(0)
    ml["training_completion_flag"] = ml["training_completion_flag"].fillna(0).astype("Int64")
    ml["promotion_flag"] = ml["promotion_flag"].fillna(0).astype("Int64")

    target_columns = [
        "employee_id",
        "age",
        "gender",
        "department_name",
        "job_role",
        "job_level",
        "location",
        "work_mode",
        "tenure_years",
        "annual_salary",
        "salary_band",
        "absence_rate",
        "late_arrivals",
        "training_hours",
        "training_completion_flag",
        "training_completion_rate",
        "performance_rating",
        "potential_rating",
        "promotion_flag",
        "attrition_flag",
    ]

    ml = ml[target_columns].rename(columns={"department_name": "department"})

    return ml.sort_values("employee_id")


def create_relationship_validation(gold_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create simple relationship validation checks for Gold tables."""
    checks = []

    def add_check(table_name: str, check_name: str, issue_count: int) -> None:
        checks.append(
            {
                "table_name": table_name,
                "check_name": check_name,
                "issue_count": int(issue_count),
                "status": "Pass" if int(issue_count) == 0 else "Review",
            }
        )

    key_checks = {
        "fact_payroll": ["employee_key", "pay_period_key"],
        "fact_attendance": ["employee_key", "attendance_month_key"],
        "fact_leave": ["employee_key", "leave_start_date_key", "leave_end_date_key"],
        "fact_recruitment": ["department_key", "job_role_key", "location_key"],
        "fact_training": ["employee_key", "assigned_date_key"],
        "fact_performance": ["employee_key"],
        "fact_attrition": ["employee_key", "exit_date_key"],
    }

    for table_name, columns in key_checks.items():
        table = gold_tables.get(table_name)
        if table is None:
            continue
        for column in columns:
            if column in table.columns:
                add_check(table_name, f"Missing {column}", table[column].isna().sum())

    dim_employee = gold_tables.get("dim_employee")
    if dim_employee is not None:
        add_check(
            "dim_employee",
            "Duplicate employee_id",
            dim_employee["employee_id"].duplicated().sum(),
        )

    dim_date = gold_tables.get("dim_date")
    if dim_date is not None:
        add_check(
            "dim_date",
            "Duplicate date_key",
            dim_date["date_key"].duplicated().sum(),
        )

    return pd.DataFrame(checks)


def create_gold_build_summary(gold_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create a summary of Gold table row and column counts."""
    rows = []
    for table_name, dataframe in gold_tables.items():
        rows.append(
            {
                "table_name": table_name,
                "row_count": len(dataframe),
                "column_count": len(dataframe.columns),
            }
        )
    return pd.DataFrame(rows).sort_values("table_name")


def run_silver_to_gold() -> None:
    """Run Silver to Gold dimensional modelling."""
    print("Starting Silver to Gold dimensional modelling...")

    source_tables = clean_source_tables()
    source_tables["employees"] = enrich_employee_fields(source_tables["employees"])

    employees = source_tables["employees"]
    payroll = source_tables["payroll"]
    attendance = source_tables["attendance"]
    leave_df = source_tables["leave"]
    recruitment = source_tables["recruitment"]
    training = source_tables["training"]
    performance = source_tables["performance"]
    attrition = source_tables["attrition"]
    security = source_tables["security_mapping"]

    dim_department = create_dim_department(employees, recruitment)
    dim_job_role = create_dim_job_role(employees, recruitment)
    dim_location = create_dim_location(employees, recruitment)
    dim_manager = create_dim_manager(employees)
    dim_security_user = create_dim_security_user(security)
    dim_employee = create_dim_employee(
        employees,
        dim_department,
        dim_job_role,
        dim_location,
        dim_manager,
    )
    dim_date = create_dim_date(source_tables)

    lookups = create_lookup_maps(
        dim_employee,
        dim_department,
        dim_job_role,
        dim_location,
        dim_manager,
    )

    fact_payroll = create_fact_payroll(payroll, lookups)
    fact_attendance = create_fact_attendance(attendance, lookups)
    fact_leave = create_fact_leave(leave_df, lookups)
    fact_recruitment = create_fact_recruitment(recruitment, lookups)
    fact_training = create_fact_training(training, lookups)
    fact_performance = create_fact_performance(performance, lookups)
    fact_attrition = create_fact_attrition(attrition, lookups)

    ml_attrition_dataset = create_ml_attrition_dataset(
        dim_employee,
        dim_department,
        dim_job_role,
        dim_location,
        fact_payroll,
        fact_attendance,
        fact_training,
        fact_performance,
        fact_attrition,
    )

    gold_tables = {
        "dim_employee": dim_employee,
        "dim_department": dim_department,
        "dim_job_role": dim_job_role,
        "dim_location": dim_location,
        "dim_date": dim_date,
        "dim_manager": dim_manager,
        "dim_security_user": dim_security_user,
        "fact_payroll": fact_payroll,
        "fact_attendance": fact_attendance,
        "fact_leave": fact_leave,
        "fact_recruitment": fact_recruitment,
        "fact_training": fact_training,
        "fact_performance": fact_performance,
        "fact_attrition": fact_attrition,
        "ml_attrition_dataset": ml_attrition_dataset,
    }

    for table_name, dataframe in gold_tables.items():
        write_gold_table(dataframe, table_name)
        print(f"Created data/gold/{table_name}.csv ({len(dataframe):,} rows)")

    relationship_validation = create_relationship_validation(gold_tables)
    build_summary = create_gold_build_summary(gold_tables)

    write_gold_table(relationship_validation, "gold_relationship_validation")
    write_gold_table(build_summary, "gold_build_summary")

    review_count = int((relationship_validation["status"] == "Review").sum())

    print("\nSilver to Gold dimensional modelling completed successfully.")
    print(f"Gold tables created: {len(gold_tables)}")
    print(f"Relationship checks needing review: {review_count}")
    print("Build summary: data/gold/gold_build_summary.csv")
    print("Relationship validation: data/gold/gold_relationship_validation.csv")


if __name__ == "__main__":
    run_silver_to_gold()
