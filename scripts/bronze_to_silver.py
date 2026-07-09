from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"
SILVER_DIR = PROJECT_ROOT / "data" / "silver"

REFERENCE_DATE = pd.Timestamp("2026-06-30")


BRONZE_FILES = {
    "employees": "bronze_employees.csv",
    "payroll": "bronze_payroll.csv",
    "attendance": "bronze_attendance.csv",
    "leave": "bronze_leave.csv",
    "recruitment": "bronze_recruitment.csv",
    "training": "bronze_training.csv",
    "performance": "bronze_performance.csv",
    "attrition": "bronze_attrition.csv",
    "security_mapping": "bronze_security_mapping.csv",
}


VALID_DEPARTMENTS = {
    "HR",
    "Finance",
    "Sales",
    "Marketing",
    "IT",
    "Operations",
    "Customer Support",
    "Legal",
}

VALID_LOCATIONS = {
    "London",
    "Manchester",
    "Birmingham",
    "Leeds",
    "Bristol",
    "Edinburgh",
}

VALID_WORK_MODES = {"Office", "Hybrid", "Remote"}
VALID_EMPLOYMENT_TYPES = {"Full-time", "Part-time", "Contract"}
VALID_EMPLOYEE_STATUSES = {"Active", "Left"}

VALID_LEAVE_TYPES = {"Annual", "Sick", "Unpaid", "Maternity", "Paternity", "Other"}
VALID_LEAVE_STATUSES = {"Approved", "Rejected", "Pending"}

VALID_RECRUITMENT_SOURCES = {
    "Job Board",
    "Referral",
    "LinkedIn",
    "Agency",
    "Campus",
    "Company Website",
}
VALID_RECRUITMENT_STATUSES = {"Applied", "Interviewed", "Offered", "Hired", "Rejected"}

VALID_COURSE_CATEGORIES = {
    "Technical",
    "Compliance",
    "Leadership",
    "HR",
    "Finance",
    "Soft Skills",
}
VALID_TRAINING_STATUSES = {"Completed", "In Progress", "Not Started", "Overdue"}

VALID_REVIEW_PERIODS = {"Annual", "Mid-Year", "Quarterly"}

VALID_EXIT_REASONS = {
    "Resignation",
    "Better Opportunity",
    "Retirement",
    "Termination",
    "Relocation",
    "Personal Reasons",
    "Other",
}
VALID_ATTRITION_TYPES = {"Voluntary", "Involuntary"}

VALID_ACCESS_TYPES = {"ALL", "DEPARTMENT", "LOCATION", "RESTRICTED"}

SALARY_BAND_SORT = {
    "Under 30K": 1,
    "30K-40K": 2,
    "40K-50K": 3,
    "50K-65K": 4,
    "65K-80K": 5,
    "80K-100K": 6,
    "100K+": 7,
}


def read_bronze_table(dataset_name: str) -> pd.DataFrame:
    """Read a Bronze CSV file as text before Silver type conversion."""
    file_name = BRONZE_FILES[dataset_name]
    path = BRONZE_DIR / file_name

    if not path.exists():
        raise FileNotFoundError(f"Bronze file not found: {path}")

    return pd.read_csv(path, dtype=str)


def normalise_blank_values(df: pd.DataFrame) -> pd.DataFrame:
    """Trim text values and convert blank strings to missing values."""
    output = df.copy()

    for column in output.columns:
        if output[column].dtype == "object":
            output[column] = output[column].astype("string").str.strip()
            output[column] = output[column].replace(
                {"": pd.NA, "nan": pd.NA, "None": pd.NA}
            )

    return output


def parse_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to date values."""
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


def add_quality_check(
    checks: list[dict],
    dataset: str,
    check_name: str,
    issue_count: int,
    severity: str = "Error",
) -> None:
    """Add one data quality check result."""
    checks.append(
        {
            "dataset": dataset,
            "check_name": check_name,
            "issue_count": int(issue_count),
            "severity": severity,
            "status": "Pass" if int(issue_count) == 0 else "Review",
        }
    )


def count_invalid_values(series: pd.Series, valid_values: set[str]) -> int:
    """Count values that are not missing and not in the allowed value list."""
    return int((series.notna() & ~series.isin(valid_values)).sum())


def count_missing_employee_references(
    df: pd.DataFrame,
    valid_employee_ids: set[str],
    column: str = "employee_id",
) -> int:
    """Count employee IDs that do not exist in the employee master table."""
    if column not in df.columns:
        return 0

    values = set(df[column].dropna().astype(str))
    return len(values - valid_employee_ids)


def calculate_age(date_of_birth: pd.Series) -> pd.Series:
    """Calculate employee age at the reference date."""
    return np.floor((REFERENCE_DATE - date_of_birth).dt.days / 365.25)


def calculate_tenure(hire_date: pd.Series, end_date: pd.Series) -> pd.Series:
    """Calculate employee tenure in years."""
    return ((end_date - hire_date).dt.days / 365.25).round(2)


def clean_attrition(checks: list[dict]) -> pd.DataFrame:
    attrition = normalise_blank_values(read_bronze_table("attrition"))

    attrition = parse_dates(attrition, ["exit_date"])
    attrition = parse_numbers(
        attrition,
        ["regrettable_attrition_flag", "notice_period_days"],
    )

    add_quality_check(
        checks,
        "attrition",
        "Missing employee_id",
        attrition["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "attrition",
        "Invalid exit_reason",
        count_invalid_values(attrition["exit_reason"], VALID_EXIT_REASONS),
        "Warning",
    )
    add_quality_check(
        checks,
        "attrition",
        "Invalid attrition_type",
        count_invalid_values(attrition["attrition_type"], VALID_ATTRITION_TYPES),
    )

    attrition["attrition_flag"] = 1
    attrition["regrettable_attrition_flag"] = (
        attrition["regrettable_attrition_flag"].fillna(0).astype(int)
    )
    attrition["notice_period_days"] = attrition["notice_period_days"].fillna(0).astype(int)

    return attrition


def clean_employees(attrition: pd.DataFrame, checks: list[dict]) -> pd.DataFrame:
    employees = normalise_blank_values(read_bronze_table("employees"))

    employees = parse_dates(employees, ["date_of_birth", "hire_date"])

    add_quality_check(
        checks,
        "employees",
        "Missing employee_id",
        employees["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "employees",
        "Duplicate employee_id",
        employees["employee_id"].duplicated().sum(),
    )
    add_quality_check(
        checks,
        "employees",
        "Future hire_date",
        (employees["hire_date"] > REFERENCE_DATE).sum(),
    )
    add_quality_check(
        checks,
        "employees",
        "Invalid department",
        count_invalid_values(employees["department"], VALID_DEPARTMENTS),
    )
    add_quality_check(
        checks,
        "employees",
        "Invalid location",
        count_invalid_values(employees["location"], VALID_LOCATIONS),
    )
    add_quality_check(
        checks,
        "employees",
        "Invalid work_mode",
        count_invalid_values(employees["work_mode"], VALID_WORK_MODES),
    )
    add_quality_check(
        checks,
        "employees",
        "Invalid employment_type",
        count_invalid_values(employees["employment_type"], VALID_EMPLOYMENT_TYPES),
        "Warning",
    )
    add_quality_check(
        checks,
        "employees",
        "Invalid employee_status",
        count_invalid_values(employees["employee_status"], VALID_EMPLOYEE_STATUSES),
    )

    employees = employees.dropna(subset=["employee_id"])
    employees = employees.drop_duplicates(subset=["employee_id"], keep="first")

    exit_dates = attrition[["employee_id", "exit_date"]].drop_duplicates("employee_id")
    employees = employees.merge(exit_dates, on="employee_id", how="left")

    employees.loc[employees["exit_date"].notna(), "employee_status"] = "Left"
    employees["employee_status"] = employees["employee_status"].fillna("Active")

    employees["full_name"] = (
        employees["first_name"].fillna("").astype(str).str.strip()
        + " "
        + employees["last_name"].fillna("").astype(str).str.strip()
    ).str.strip()

    employees["age"] = calculate_age(employees["date_of_birth"]).astype("Int64")

    tenure_end_date = employees["exit_date"].fillna(REFERENCE_DATE)
    employees["tenure_years"] = calculate_tenure(
        employees["hire_date"],
        tenure_end_date,
    )

    valid_employee_ids = set(employees["employee_id"])

    invalid_manager_count = int(
        employees["manager_id"].notna().sum()
        - employees.loc[
            employees["manager_id"].isin(valid_employee_ids),
            "manager_id",
        ].count()
    )

    add_quality_check(
        checks,
        "employees",
        "manager_id not found in employees",
        invalid_manager_count,
        "Warning",
    )

    return employees


def clean_payroll(valid_employee_ids: set[str], checks: list[dict]) -> pd.DataFrame:
    payroll = normalise_blank_values(read_bronze_table("payroll"))

    payroll = parse_dates(payroll, ["pay_period"])
    payroll = parse_numbers(
        payroll,
        ["annual_salary", "monthly_salary", "bonus_amount"],
    )

    add_quality_check(
        checks,
        "payroll",
        "Missing employee_id",
        payroll["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "payroll",
        "Employee ID not found in employee master",
        count_missing_employee_references(payroll, valid_employee_ids),
    )
    add_quality_check(
        checks,
        "payroll",
        "Annual salary less than or equal to zero",
        (payroll["annual_salary"] <= 0).sum(),
    )

    payroll = payroll[payroll["employee_id"].isin(valid_employee_ids)].copy()

    payroll["monthly_salary"] = payroll["monthly_salary"].fillna(
        (payroll["annual_salary"] / 12).round(2)
    )
    payroll["bonus_amount"] = payroll["bonus_amount"].fillna(0)
    payroll["salary_band_sort_order"] = payroll["salary_band"].map(SALARY_BAND_SORT).astype(
        "Int64"
    )

    return payroll


def clean_attendance(valid_employee_ids: set[str], checks: list[dict]) -> pd.DataFrame:
    attendance = normalise_blank_values(read_bronze_table("attendance"))

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
        ],
    )

    add_quality_check(
        checks,
        "attendance",
        "Missing employee_id",
        attendance["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "attendance",
        "Employee ID not found in employee master",
        count_missing_employee_references(attendance, valid_employee_ids),
    )
    add_quality_check(
        checks,
        "attendance",
        "Working days less than or equal to zero",
        (attendance["working_days"] <= 0).sum(),
    )
    add_quality_check(
        checks,
        "attendance",
        "Present plus absent days greater than working days",
        ((attendance["present_days"] + attendance["absent_days"]) > attendance["working_days"]).sum(),
    )

    attendance = attendance[attendance["employee_id"].isin(valid_employee_ids)].copy()

    attendance["attendance_rate"] = (
        attendance["present_days"] / attendance["working_days"]
    ).round(4)
    attendance["absence_rate"] = (
        attendance["absent_days"] / attendance["working_days"]
    ).round(4)

    return attendance


def clean_leave(valid_employee_ids: set[str], checks: list[dict]) -> pd.DataFrame:
    leave_df = normalise_blank_values(read_bronze_table("leave"))

    leave_df = parse_dates(leave_df, ["leave_start_date", "leave_end_date"])
    leave_df = parse_numbers(leave_df, ["leave_days"])

    add_quality_check(
        checks,
        "leave",
        "Missing employee_id",
        leave_df["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "leave",
        "Employee ID not found in employee master",
        count_missing_employee_references(leave_df, valid_employee_ids),
    )
    add_quality_check(
        checks,
        "leave",
        "leave_end_date before leave_start_date",
        (leave_df["leave_end_date"] < leave_df["leave_start_date"]).sum(),
    )
    add_quality_check(
        checks,
        "leave",
        "Invalid leave_type",
        count_invalid_values(leave_df["leave_type"], VALID_LEAVE_TYPES),
        "Warning",
    )
    add_quality_check(
        checks,
        "leave",
        "Invalid leave_status",
        count_invalid_values(leave_df["leave_status"], VALID_LEAVE_STATUSES),
        "Warning",
    )

    leave_df = leave_df[leave_df["employee_id"].isin(valid_employee_ids)].copy()

    calculated_leave_days = (
        leave_df["leave_end_date"] - leave_df["leave_start_date"]
    ).dt.days + 1

    leave_df["leave_days"] = leave_df["leave_days"].fillna(calculated_leave_days).astype(
        "Int64"
    )
    leave_df["leave_year"] = leave_df["leave_start_date"].dt.year.astype("Int64")

    return leave_df


def clean_recruitment(valid_employee_ids: set[str], checks: list[dict]) -> pd.DataFrame:
    recruitment = normalise_blank_values(read_bronze_table("recruitment"))

    recruitment = parse_dates(
        recruitment,
        ["application_date", "interview_date", "offer_date", "hire_date"],
    )
    recruitment = parse_numbers(recruitment, ["time_to_hire_days"])

    add_quality_check(
        checks,
        "recruitment",
        "Invalid recruitment_source",
        count_invalid_values(
            recruitment["recruitment_source"],
            VALID_RECRUITMENT_SOURCES,
        ),
        "Warning",
    )
    add_quality_check(
        checks,
        "recruitment",
        "Invalid status",
        count_invalid_values(recruitment["status"], VALID_RECRUITMENT_STATUSES),
    )
    add_quality_check(
        checks,
        "recruitment",
        "application_date after hire_date",
        (recruitment["application_date"] > recruitment["hire_date"]).sum(),
    )

    hired_mask = recruitment["status"].eq("Hired") & recruitment["hired_employee_id"].notna()

    missing_hired_employee = int(
        (hired_mask & ~recruitment["hired_employee_id"].isin(valid_employee_ids)).sum()
    )

    add_quality_check(
        checks,
        "recruitment",
        "hired_employee_id not found in employee master",
        missing_hired_employee,
        "Warning",
    )

    calculated_time_to_hire = (
        recruitment["hire_date"] - recruitment["application_date"]
    ).dt.days

    recruitment["time_to_hire_days"] = recruitment["time_to_hire_days"].fillna(
        calculated_time_to_hire
    ).astype("Int64")

    return recruitment


def clean_training(valid_employee_ids: set[str], checks: list[dict]) -> pd.DataFrame:
    training = normalise_blank_values(read_bronze_table("training"))

    training = parse_dates(training, ["assigned_date", "completion_date"])
    training = parse_numbers(training, ["training_hours", "training_score"])

    add_quality_check(
        checks,
        "training",
        "Missing employee_id",
        training["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "training",
        "Employee ID not found in employee master",
        count_missing_employee_references(training, valid_employee_ids),
    )
    add_quality_check(
        checks,
        "training",
        "completion_date before assigned_date",
        (training["completion_date"] < training["assigned_date"]).sum(),
    )
    add_quality_check(
        checks,
        "training",
        "Invalid course_category",
        count_invalid_values(training["course_category"], VALID_COURSE_CATEGORIES),
        "Warning",
    )
    add_quality_check(
        checks,
        "training",
        "Invalid completion_status",
        count_invalid_values(training["completion_status"], VALID_TRAINING_STATUSES),
        "Warning",
    )

    training = training[training["employee_id"].isin(valid_employee_ids)].copy()

    training["completion_flag"] = np.where(
        training["completion_status"].eq("Completed"),
        1,
        0,
    )
    training["training_score"] = training["training_score"].clip(lower=0, upper=100)

    return training


def clean_performance(valid_employee_ids: set[str], checks: list[dict]) -> pd.DataFrame:
    performance = normalise_blank_values(read_bronze_table("performance"))

    performance = parse_numbers(
        performance,
        ["review_year", "performance_rating", "potential_rating", "promotion_flag"],
    )

    add_quality_check(
        checks,
        "performance",
        "Missing employee_id",
        performance["employee_id"].isna().sum(),
    )
    add_quality_check(
        checks,
        "performance",
        "Employee ID not found in employee master",
        count_missing_employee_references(performance, valid_employee_ids),
    )
    add_quality_check(
        checks,
        "performance",
        "performance_rating outside 1 to 5",
        (~performance["performance_rating"].between(1, 5)).sum(),
    )
    add_quality_check(
        checks,
        "performance",
        "potential_rating outside 1 to 5",
        (~performance["potential_rating"].between(1, 5)).sum(),
    )
    add_quality_check(
        checks,
        "performance",
        "Invalid review_period",
        count_invalid_values(performance["review_period"], VALID_REVIEW_PERIODS),
        "Warning",
    )

    performance = performance[performance["employee_id"].isin(valid_employee_ids)].copy()

    performance["review_year"] = performance["review_year"].astype("Int64")
    performance["performance_rating"] = performance["performance_rating"].astype("Int64")
    performance["potential_rating"] = performance["potential_rating"].astype("Int64")
    performance["promotion_flag"] = performance["promotion_flag"].fillna(0).astype(int)

    return performance


def clean_security_mapping(checks: list[dict]) -> pd.DataFrame:
    security = normalise_blank_values(read_bronze_table("security_mapping"))

    security["user_email"] = security["user_email"].str.lower()
    security["access_type"] = security["access_type"].str.upper()

    add_quality_check(
        checks,
        "security_mapping",
        "Missing user_email",
        security["user_email"].isna().sum(),
    )
    add_quality_check(
        checks,
        "security_mapping",
        "Invalid email format",
        (~security["user_email"].str.contains("@", na=False)).sum(),
    )
    add_quality_check(
        checks,
        "security_mapping",
        "Invalid access_type",
        count_invalid_values(security["access_type"], VALID_ACCESS_TYPES),
    )

    security = security.dropna(subset=["user_email"])
    security = security.drop_duplicates(
        subset=["user_email", "access_type", "department", "location"]
    )

    return security


def write_silver_table(df: pd.DataFrame, table_name: str) -> None:
    """Write a Silver dataframe to CSV."""
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    output = df.copy()

    for column in output.columns:
        if pd.api.types.is_datetime64_any_dtype(output[column]):
            output[column] = output[column].dt.strftime("%Y-%m-%d")

    output.to_csv(SILVER_DIR / f"silver_{table_name}.csv", index=False)


def run_bronze_to_silver() -> None:
    """Run Bronze to Silver cleaning and validation."""
    print("Starting Bronze to Silver cleaning...")

    checks: list[dict] = []

    attrition = clean_attrition(checks)
    employees = clean_employees(attrition, checks)

    valid_employee_ids = set(employees["employee_id"].dropna().astype(str))

    payroll = clean_payroll(valid_employee_ids, checks)
    attendance = clean_attendance(valid_employee_ids, checks)
    leave_df = clean_leave(valid_employee_ids, checks)
    recruitment = clean_recruitment(valid_employee_ids, checks)
    training = clean_training(valid_employee_ids, checks)
    performance = clean_performance(valid_employee_ids, checks)
    security = clean_security_mapping(checks)

    add_quality_check(
        checks,
        "attrition",
        "Employee ID not found in employee master",
        count_missing_employee_references(attrition, valid_employee_ids),
    )

    attrition = attrition[attrition["employee_id"].isin(valid_employee_ids)].copy()

    output_tables = {
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

    for table_name, dataframe in output_tables.items():
        write_silver_table(dataframe, table_name)
        print(f"Created data/silver/silver_{table_name}.csv ({len(dataframe):,} rows)")

    quality_summary = pd.DataFrame(checks)
    quality_summary.to_csv(SILVER_DIR / "silver_data_quality_summary.csv", index=False)

    issue_count = int(quality_summary["issue_count"].sum()) if not quality_summary.empty else 0
    review_checks = int((quality_summary["status"] == "Review").sum()) if not quality_summary.empty else 0

    print("\nBronze to Silver cleaning completed successfully.")
    print(f"Data quality checks created: {len(quality_summary)}")
    print(f"Checks needing review: {review_checks}")
    print(f"Total issue count: {issue_count}")
    print("Data quality summary: data/silver/silver_data_quality_summary.csv")


if __name__ == "__main__":
    run_bronze_to_silver()