
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
NUM_EMPLOYEES = 600
REFERENCE_DATE = pd.Timestamp("2026-06-30")
HISTORY_START_DATE = pd.Timestamp("2024-01-01")
HIRE_DATE_START = pd.Timestamp("2017-01-01")

RNG = np.random.default_rng(RANDOM_SEED)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


FIRST_NAMES = [
    "Olivia", "Amelia", "Isla", "Ava", "Mia", "Sophia", "Grace", "Freya",
    "Lily", "Ella", "Noah", "Oliver", "George", "Arthur", "Muhammad", "Leo",
    "Oscar", "Harry", "Archie", "Jack", "Aarav", "Diya", "Ishaan", "Anaya",
    "Rohan", "Priya", "Sofia", "Luca", "Maya", "Ethan"
]

LAST_NAMES = [
    "Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson",
    "Davies", "Patel", "Khan", "Singh", "Shah", "Thomas", "Roberts",
    "Walker", "Wright", "Thompson", "White", "Green", "Hall", "Clark",
    "Lewis", "Harris", "Martin", "Jackson", "Young", "King", "Scott"
]

DEPARTMENTS = [
    "HR",
    "Finance",
    "Sales",
    "Marketing",
    "IT",
    "Operations",
    "Customer Support",
    "Legal",
]

DEPARTMENT_WEIGHTS = [0.08, 0.10, 0.18, 0.10, 0.18, 0.18, 0.13, 0.05]

JOB_LEVELS = ["Junior", "Mid", "Senior", "Manager", "Director"]
JOB_LEVEL_WEIGHTS = [0.25, 0.35, 0.25, 0.12, 0.03]

ROLE_BY_DEPARTMENT_LEVEL = {
    "HR": {
        "Junior": "HR Assistant",
        "Mid": "HR Advisor",
        "Senior": "HR Business Partner",
        "Manager": "HR Manager",
        "Director": "HR Director",
    },
    "Finance": {
        "Junior": "Accounts Assistant",
        "Mid": "Finance Analyst",
        "Senior": "Senior Finance Analyst",
        "Manager": "Finance Manager",
        "Director": "Finance Director",
    },
    "Sales": {
        "Junior": "Sales Development Representative",
        "Mid": "Sales Executive",
        "Senior": "Senior Account Executive",
        "Manager": "Sales Manager",
        "Director": "Sales Director",
    },
    "Marketing": {
        "Junior": "Marketing Assistant",
        "Mid": "Marketing Executive",
        "Senior": "Senior Marketing Specialist",
        "Manager": "Marketing Manager",
        "Director": "Marketing Director",
    },
    "IT": {
        "Junior": "Junior Software Developer",
        "Mid": "Data Analyst",
        "Senior": "Senior Data Engineer",
        "Manager": "IT Manager",
        "Director": "Technology Director",
    },
    "Operations": {
        "Junior": "Operations Assistant",
        "Mid": "Operations Analyst",
        "Senior": "Senior Operations Specialist",
        "Manager": "Operations Manager",
        "Director": "Operations Director",
    },
    "Customer Support": {
        "Junior": "Customer Support Advisor",
        "Mid": "Customer Support Specialist",
        "Senior": "Senior Support Specialist",
        "Manager": "Customer Support Manager",
        "Director": "Customer Experience Director",
    },
    "Legal": {
        "Junior": "Legal Assistant",
        "Mid": "Legal Advisor",
        "Senior": "Senior Legal Counsel",
        "Manager": "Legal Manager",
        "Director": "Legal Director",
    },
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

LOCATIONS = ["London", "Manchester", "Birmingham", "Leeds", "Bristol", "Edinburgh"]
LOCATION_WEIGHTS = [0.30, 0.20, 0.18, 0.12, 0.10, 0.10]

LOCATION_REGION = {
    "London": "London and South East",
    "Manchester": "North West",
    "Birmingham": "West Midlands",
    "Leeds": "Yorkshire and Humber",
    "Bristol": "South West",
    "Edinburgh": "Scotland",
}

WORK_MODES = ["Office", "Hybrid", "Remote"]
WORK_MODE_WEIGHTS = [0.35, 0.45, 0.20]

EMPLOYMENT_TYPES = ["Full-time", "Part-time", "Contract"]
EMPLOYMENT_TYPE_WEIGHTS = [0.82, 0.12, 0.06]

GENDERS = ["Female", "Male", "Other", "Not disclosed"]
GENDER_WEIGHTS = [0.48, 0.48, 0.02, 0.02]

SALARY_RANGE_BY_LEVEL = {
    "Junior": (24000, 33000),
    "Mid": (33000, 48000),
    "Senior": (48000, 68000),
    "Manager": (65000, 90000),
    "Director": (90000, 135000),
}

PAY_GRADE_BY_LEVEL = {
    "Junior": "G3",
    "Mid": "G4",
    "Senior": "G5",
    "Manager": "G6",
    "Director": "G7",
}

DEPARTMENT_SALARY_MULTIPLIER = {
    "HR": 0.95,
    "Finance": 1.06,
    "Sales": 1.05,
    "Marketing": 0.98,
    "IT": 1.12,
    "Operations": 0.97,
    "Customer Support": 0.90,
    "Legal": 1.15,
}

LOCATION_SALARY_MULTIPLIER = {
    "London": 1.12,
    "Manchester": 1.00,
    "Birmingham": 0.96,
    "Leeds": 0.95,
    "Bristol": 0.98,
    "Edinburgh": 0.97,
}

COURSES_BY_CATEGORY = {
    "Compliance": ["Data Protection Training", "Workplace Health and Safety", "Information Security Awareness"],
    "Technical": ["Power BI Fundamentals", "SQL for Analysts", "Cloud Data Fundamentals", "Python for Data Analysis"],
    "Leadership": ["First Line Manager Training", "Coaching Skills", "Leading High Performing Teams"],
    "HR": ["Inclusive Hiring", "Employee Relations Essentials"],
    "Finance": ["Budget Management", "Financial Controls"],
    "Soft Skills": ["Communication Skills", "Presentation Skills", "Stakeholder Management"],
}


def random_date(start: pd.Timestamp, end: pd.Timestamp) -> pd.Timestamp:
    """Return a random date between start and end, inclusive."""
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    if end < start:
        return start

    start_ordinal = start.toordinal()
    end_ordinal = end.toordinal()
    return pd.Timestamp.fromordinal(int(RNG.integers(start_ordinal, end_ordinal + 1)))


def month_start_range(start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
    """Return month-start dates between start and end."""
    start_month = pd.Timestamp(start).replace(day=1)
    end_month = pd.Timestamp(end).replace(day=1)
    if end_month < start_month:
        return pd.DatetimeIndex([])
    return pd.date_range(start_month, end_month, freq="MS")


def salary_band(annual_salary: float) -> str:
    """Convert annual salary into a reporting salary band."""
    if annual_salary < 30000:
        return "Under 30K"
    if annual_salary < 40000:
        return "30K-40K"
    if annual_salary < 50000:
        return "40K-50K"
    if annual_salary < 65000:
        return "50K-65K"
    if annual_salary < 80000:
        return "65K-80K"
    if annual_salary < 100000:
        return "80K-100K"
    return "100K+"


def generate_employee_master() -> pd.DataFrame:
    """Generate synthetic employee master data with internal modelling fields."""
    records = []

    for index in range(1, NUM_EMPLOYEES + 1):
        employee_id = f"EMP{index:04d}"
        first_name = str(RNG.choice(FIRST_NAMES))
        last_name = str(RNG.choice(LAST_NAMES))
        gender = str(RNG.choice(GENDERS, p=GENDER_WEIGHTS))
        department = str(RNG.choice(DEPARTMENTS, p=DEPARTMENT_WEIGHTS))
        job_level = str(RNG.choice(JOB_LEVELS, p=JOB_LEVEL_WEIGHTS))
        job_role = ROLE_BY_DEPARTMENT_LEVEL[department][job_level]
        location = str(RNG.choice(LOCATIONS, p=LOCATION_WEIGHTS))
        work_mode = str(RNG.choice(WORK_MODES, p=WORK_MODE_WEIGHTS))
        employment_type = str(RNG.choice(EMPLOYMENT_TYPES, p=EMPLOYMENT_TYPE_WEIGHTS))

        age = int(np.clip(RNG.normal(38, 9), 22, 64))
        date_of_birth = REFERENCE_DATE - pd.DateOffset(years=age) - pd.DateOffset(days=int(RNG.integers(0, 365)))

        hire_date = random_date(HIRE_DATE_START, REFERENCE_DATE - pd.DateOffset(months=2))

        salary_low, salary_high = SALARY_RANGE_BY_LEVEL[job_level]
        annual_salary = float(RNG.uniform(salary_low, salary_high))
        annual_salary *= DEPARTMENT_SALARY_MULTIPLIER[department]
        annual_salary *= LOCATION_SALARY_MULTIPLIER[location]
        annual_salary = round(annual_salary / 500) * 500

        performance_base = float(np.clip(RNG.normal(3.4, 0.75), 1.0, 5.0))
        absence_tendency = float(np.clip(RNG.beta(2, 18), 0.01, 0.20))
        training_interest = float(np.clip(RNG.beta(5, 3), 0.05, 1.0))

        records.append(
            {
                "employee_id": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "date_of_birth": date_of_birth.normalize(),
                "hire_date": hire_date.normalize(),
                "department": department,
                "job_role": job_role,
                "job_level": job_level,
                "location": location,
                "country": "United Kingdom",
                "work_mode": work_mode,
                "manager_id": "",
                "employment_type": employment_type,
                "employee_status": "Active",
                "email": f"{employee_id.lower()}@abcglobal.com",
                "_annual_salary": annual_salary,
                "_pay_grade": PAY_GRADE_BY_LEVEL[job_level],
                "_salary_band": salary_band(annual_salary),
                "_performance_base": performance_base,
                "_absence_tendency": absence_tendency,
                "_training_interest": training_interest,
            }
        )

    employees = pd.DataFrame(records)
    employees = assign_managers(employees)
    employees = assign_employee_status(employees)
    return employees


def assign_managers(employees: pd.DataFrame) -> pd.DataFrame:
    """Assign manager IDs based on department and job level."""
    employees = employees.copy()

    for idx, employee in employees.iterrows():
        department = employee["department"]
        job_level = employee["job_level"]
        employee_id = employee["employee_id"]

        if job_level == "Director":
            employees.at[idx, "manager_id"] = ""
            continue

        if job_level == "Manager":
            manager_pool = employees[
                (employees["department"] == department)
                & (employees["job_level"] == "Director")
                & (employees["employee_id"] != employee_id)
            ]
        else:
            manager_pool = employees[
                (employees["department"] == department)
                & (employees["job_level"].isin(["Manager", "Director"]))
                & (employees["employee_id"] != employee_id)
            ]

        if not manager_pool.empty:
            employees.at[idx, "manager_id"] = str(RNG.choice(manager_pool["employee_id"].to_numpy()))
        else:
            employees.at[idx, "manager_id"] = ""

    return employees


def assign_employee_status(employees: pd.DataFrame) -> pd.DataFrame:
    """Assign active/left status using realistic attrition risk signals."""
    employees = employees.copy()
    salary_median_by_department = employees.groupby("department")["_annual_salary"].transform("median")

    statuses = []
    exit_dates = []

    for _, employee in employees.iterrows():
        tenure_years = max((REFERENCE_DATE - employee["hire_date"]).days / 365.25, 0)

        risk = 0.07

        if tenure_years < 1:
            risk += 0.04
        elif tenure_years < 2:
            risk += 0.03

        if employee["_performance_base"] < 2.7:
            risk += 0.10
        if employee["_absence_tendency"] > 0.10:
            risk += 0.07
        if employee["_training_interest"] < 0.40:
            risk += 0.04
        if employee["_annual_salary"] < salary_median_by_department.loc[employee.name]:
            risk += 0.03
        if employee["work_mode"] == "Office":
            risk += 0.02

        risk = min(risk, 0.38)

        earliest_exit = max(employee["hire_date"] + pd.DateOffset(months=6), HISTORY_START_DATE)
        can_leave = earliest_exit < REFERENCE_DATE

        if can_leave and RNG.random() < risk:
            statuses.append("Left")
            exit_dates.append(random_date(earliest_exit, REFERENCE_DATE))
        else:
            statuses.append("Active")
            exit_dates.append(pd.NaT)

    employees["employee_status"] = statuses
    employees["_exit_date"] = exit_dates

    return employees


def generate_attrition(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate attrition records for employees marked as Left."""
    exit_reasons = [
        "Resignation",
        "Better Opportunity",
        "Retirement",
        "Termination",
        "Relocation",
        "Personal Reasons",
        "Other",
    ]
    exit_reason_weights = [0.25, 0.32, 0.08, 0.12, 0.08, 0.10, 0.05]

    records = []
    leavers = employees[employees["employee_status"] == "Left"].copy()

    for index, (_, employee) in enumerate(leavers.iterrows(), start=1):
        exit_reason = str(RNG.choice(exit_reasons, p=exit_reason_weights))
        attrition_type = "Involuntary" if exit_reason == "Termination" else "Voluntary"
        regrettable = 1 if exit_reason in ["Resignation", "Better Opportunity"] and employee["_performance_base"] >= 3.0 else 0
        notice_period_days = int(RNG.choice([0, 14, 30, 60, 90], p=[0.08, 0.10, 0.62, 0.15, 0.05]))

        records.append(
            {
                "attrition_id": f"EXT{index:06d}",
                "employee_id": employee["employee_id"],
                "exit_date": employee["_exit_date"],
                "exit_reason": exit_reason,
                "attrition_type": attrition_type,
                "regrettable_attrition_flag": regrettable,
                "notice_period_days": notice_period_days,
            }
        )

    return pd.DataFrame(records)


def employment_months(employee: pd.Series) -> pd.DatetimeIndex:
    """Return employment months within the reporting history window."""
    start = max(pd.Timestamp(employee["hire_date"]), HISTORY_START_DATE)
    end = pd.Timestamp(employee["_exit_date"]) if employee["employee_status"] == "Left" else REFERENCE_DATE
    return month_start_range(start, end)


def generate_payroll(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate monthly payroll records for each employee."""
    records = []
    record_id = 1

    for _, employee in employees.iterrows():
        for pay_period in employment_months(employee):
            monthly_salary = round(employee["_annual_salary"] / 12, 2)
            bonus_probability = 0.08 if employee["job_level"] in ["Junior", "Mid"] else 0.15
            bonus_amount = round(float(RNG.uniform(250, 3500)), 2) if RNG.random() < bonus_probability else 0.0

            records.append(
                {
                    "payroll_id": f"PAY{record_id:06d}",
                    "employee_id": employee["employee_id"],
                    "pay_period": pay_period,
                    "annual_salary": employee["_annual_salary"],
                    "monthly_salary": monthly_salary,
                    "bonus_amount": bonus_amount,
                    "pay_grade": employee["_pay_grade"],
                    "salary_band": employee["_salary_band"],
                    "currency": "GBP",
                }
            )
            record_id += 1

    return pd.DataFrame(records)


def generate_attendance(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate monthly attendance records for each employee."""
    records = []
    record_id = 1

    for _, employee in employees.iterrows():
        for attendance_month in employment_months(employee):
            month_end = attendance_month + pd.offsets.MonthEnd(0)
            working_days = len(pd.bdate_range(attendance_month, month_end))

            expected_absence = employee["_absence_tendency"] * working_days
            absent_days = int(np.clip(RNG.poisson(expected_absence), 0, max(working_days - 2, 0)))
            present_days = working_days - absent_days

            late_arrivals = int(np.clip(RNG.poisson(employee["_absence_tendency"] * 8), 0, 8))

            if employee["work_mode"] == "Remote":
                remote_work_days = int(np.clip(RNG.normal(present_days * 0.85, 2), 0, present_days))
            elif employee["work_mode"] == "Hybrid":
                remote_work_days = int(np.clip(RNG.normal(present_days * 0.45, 3), 0, present_days))
            else:
                remote_work_days = int(np.clip(RNG.normal(present_days * 0.10, 2), 0, present_days))

            overtime_base = 5 if employee["department"] in ["IT", "Operations", "Customer Support"] else 3
            overtime_hours = round(float(max(RNG.normal(overtime_base, 4), 0)), 1)

            records.append(
                {
                    "attendance_id": f"ATT{record_id:06d}",
                    "employee_id": employee["employee_id"],
                    "attendance_month": attendance_month,
                    "working_days": working_days,
                    "present_days": present_days,
                    "absent_days": absent_days,
                    "late_arrivals": late_arrivals,
                    "remote_work_days": remote_work_days,
                    "overtime_hours": overtime_hours,
                }
            )
            record_id += 1

    return pd.DataFrame(records)


def generate_leave(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate employee leave records."""
    leave_types = ["Annual", "Sick", "Unpaid", "Maternity", "Paternity", "Other"]
    leave_type_weights = [0.58, 0.28, 0.06, 0.02, 0.02, 0.04]
    leave_statuses = ["Approved", "Rejected", "Pending"]
    leave_status_weights = [0.88, 0.06, 0.06]

    records = []
    record_id = 1

    for _, employee in employees.iterrows():
        start_year = max(HISTORY_START_DATE.year, pd.Timestamp(employee["hire_date"]).year)
        end_date = pd.Timestamp(employee["_exit_date"]) if employee["employee_status"] == "Left" else REFERENCE_DATE
        end_year = end_date.year

        for year in range(start_year, end_year + 1):
            number_of_records = int(RNG.poisson(1.8))
            for _ in range(number_of_records):
                leave_type = str(RNG.choice(leave_types, p=leave_type_weights))

                if leave_type == "Annual":
                    leave_days = int(RNG.integers(1, 11))
                elif leave_type == "Sick":
                    leave_days = int(RNG.integers(1, 6))
                elif leave_type in ["Maternity", "Paternity"]:
                    leave_days = int(RNG.integers(10, 90))
                else:
                    leave_days = int(RNG.integers(1, 8))

                period_start = max(pd.Timestamp(f"{year}-01-01"), pd.Timestamp(employee["hire_date"]), HISTORY_START_DATE)
                period_end = min(pd.Timestamp(f"{year}-12-31"), end_date)

                if period_end <= period_start:
                    continue

                leave_start_date = random_date(period_start, period_end)
                leave_end_date = min(leave_start_date + pd.DateOffset(days=leave_days - 1), period_end)
                actual_leave_days = int((leave_end_date - leave_start_date).days + 1)

                records.append(
                    {
                        "leave_id": f"LEV{record_id:06d}",
                        "employee_id": employee["employee_id"],
                        "leave_type": leave_type,
                        "leave_start_date": leave_start_date,
                        "leave_end_date": leave_end_date,
                        "leave_days": actual_leave_days,
                        "leave_status": str(RNG.choice(leave_statuses, p=leave_status_weights)),
                    }
                )
                record_id += 1

    return pd.DataFrame(records)


def generate_recruitment(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate recruitment records, including hired candidates linked to employees."""
    records = []
    record_id = 1

    recruitment_sources = ["Job Board", "Referral", "LinkedIn", "Agency", "Campus", "Company Website"]
    source_weights = [0.25, 0.18, 0.26, 0.12, 0.08, 0.11]
    non_hired_statuses = ["Applied", "Interviewed", "Offered", "Rejected"]
    non_hired_weights = [0.20, 0.28, 0.12, 0.40]

    recent_hires = employees[employees["hire_date"] >= HISTORY_START_DATE].copy()

    for _, employee in recent_hires.iterrows():
        hire_date = pd.Timestamp(employee["hire_date"])
        application_date = hire_date - pd.DateOffset(days=int(RNG.integers(18, 75)))
        interview_date = application_date + pd.DateOffset(days=int(RNG.integers(5, 22)))
        offer_date = interview_date + pd.DateOffset(days=int(RNG.integers(3, 14)))

        records.append(
            {
                "candidate_id": f"CAND{record_id:06d}",
                "requisition_id": f"REQ{int(RNG.integers(1000, 9999))}",
                "department": employee["department"],
                "job_role": employee["job_role"],
                "location": employee["location"],
                "recruitment_source": str(RNG.choice(recruitment_sources, p=source_weights)),
                "application_date": application_date,
                "interview_date": interview_date,
                "offer_date": offer_date,
                "hire_date": hire_date,
                "status": "Hired",
                "hired_employee_id": employee["employee_id"],
                "time_to_hire_days": int((hire_date - application_date).days),
            }
        )
        record_id += 1

    additional_candidates = NUM_EMPLOYEES
    for _ in range(additional_candidates):
        department = str(RNG.choice(DEPARTMENTS, p=DEPARTMENT_WEIGHTS))
        job_level = str(RNG.choice(JOB_LEVELS, p=JOB_LEVEL_WEIGHTS))
        job_role = ROLE_BY_DEPARTMENT_LEVEL[department][job_level]
        location = str(RNG.choice(LOCATIONS, p=LOCATION_WEIGHTS))
        application_date = random_date(HISTORY_START_DATE, REFERENCE_DATE)
        status = str(RNG.choice(non_hired_statuses, p=non_hired_weights))

        interview_date = pd.NaT
        offer_date = pd.NaT
        hire_date = pd.NaT

        if status in ["Interviewed", "Offered"]:
            interview_date = application_date + pd.DateOffset(days=int(RNG.integers(5, 25)))
        if status == "Offered":
            offer_date = interview_date + pd.DateOffset(days=int(RNG.integers(3, 14)))

        records.append(
            {
                "candidate_id": f"CAND{record_id:06d}",
                "requisition_id": f"REQ{int(RNG.integers(1000, 9999))}",
                "department": department,
                "job_role": job_role,
                "location": location,
                "recruitment_source": str(RNG.choice(recruitment_sources, p=source_weights)),
                "application_date": application_date,
                "interview_date": interview_date,
                "offer_date": offer_date,
                "hire_date": hire_date,
                "status": status,
                "hired_employee_id": "",
                "time_to_hire_days": np.nan,
            }
        )
        record_id += 1

    return pd.DataFrame(records)


def generate_training(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate employee training records."""
    completion_statuses = ["Completed", "In Progress", "Not Started", "Overdue"]
    records = []
    record_id = 1

    for _, employee in employees.iterrows():
        start_date = max(pd.Timestamp(employee["hire_date"]), HISTORY_START_DATE)
        end_date = pd.Timestamp(employee["_exit_date"]) if employee["employee_status"] == "Left" else REFERENCE_DATE

        if end_date <= start_date:
            continue

        expected_trainings = 2 + int(employee["_training_interest"] * 4)
        number_of_trainings = int(RNG.integers(1, max(expected_trainings, 2) + 1))

        for _ in range(number_of_trainings):
            category = str(RNG.choice(list(COURSES_BY_CATEGORY.keys())))
            course_name = str(RNG.choice(COURSES_BY_CATEGORY[category]))
            assigned_date = random_date(start_date, end_date)

            completed_probability = min(0.35 + employee["_training_interest"] * 0.55, 0.95)
            status_probabilities = [
                completed_probability,
                max(0.10, 1 - completed_probability) * 0.35,
                max(0.10, 1 - completed_probability) * 0.35,
                max(0.10, 1 - completed_probability) * 0.30,
            ]
            status_probabilities = np.array(status_probabilities) / np.sum(status_probabilities)
            completion_status = str(RNG.choice(completion_statuses, p=status_probabilities))

            if completion_status == "Completed":
                completion_date = min(assigned_date + pd.DateOffset(days=int(RNG.integers(2, 45))), end_date)
                training_score = round(float(np.clip(RNG.normal(78, 12), 45, 100)), 1)
            else:
                completion_date = pd.NaT
                training_score = np.nan

            training_hours = round(float(RNG.uniform(1, 16)), 1)

            records.append(
                {
                    "training_id": f"TRN{record_id:06d}",
                    "employee_id": employee["employee_id"],
                    "course_name": course_name,
                    "course_category": category,
                    "assigned_date": assigned_date,
                    "completion_date": completion_date,
                    "completion_status": completion_status,
                    "training_hours": training_hours,
                    "training_score": training_score,
                }
            )
            record_id += 1

    return pd.DataFrame(records)


def generate_performance(employees: pd.DataFrame) -> pd.DataFrame:
    """Generate annual performance review records."""
    records = []
    record_id = 1
    review_periods = ["Annual", "Mid-Year"]

    for _, employee in employees.iterrows():
        hire_date = pd.Timestamp(employee["hire_date"])
        end_date = pd.Timestamp(employee["_exit_date"]) if employee["employee_status"] == "Left" else REFERENCE_DATE

        for year in range(HISTORY_START_DATE.year, REFERENCE_DATE.year + 1):
            review_date = pd.Timestamp(f"{year}-12-15")
            if review_date < hire_date or review_date > end_date:
                continue

            for review_period in review_periods:
                if review_period == "Mid-Year" and RNG.random() > 0.45:
                    continue

                rating = int(np.clip(round(RNG.normal(employee["_performance_base"], 0.55)), 1, 5))
                potential = int(np.clip(round(RNG.normal(rating, 0.70)), 1, 5))
                promotion_flag = 1 if rating >= 4 and potential >= 4 and RNG.random() < 0.18 else 0

                records.append(
                    {
                        "performance_id": f"PERF{record_id:06d}",
                        "employee_id": employee["employee_id"],
                        "review_year": year,
                        "review_period": review_period,
                        "performance_rating": rating,
                        "potential_rating": potential,
                        "promotion_flag": promotion_flag,
                        "manager_id": employee["manager_id"],
                    }
                )
                record_id += 1

    return pd.DataFrame(records)


def generate_security_mapping() -> pd.DataFrame:
    """Generate sample Power BI Row-Level Security mapping data."""
    rows = [
        {
            "user_email": "hr.director@abcglobal.com",
            "user_name": "HR Director",
            "access_type": "ALL",
            "department": "ALL",
            "location": "ALL",
            "role_description": "HR Director",
        },
        {
            "user_email": "hr.businesspartner@abcglobal.com",
            "user_name": "HR Business Partner",
            "access_type": "ALL",
            "department": "ALL",
            "location": "ALL",
            "role_description": "HR Business Partner",
        },
    ]

    for department in DEPARTMENTS:
        rows.append(
            {
                "user_email": f"manager.{department.lower().replace(' ', '')}@abcglobal.com",
                "user_name": f"{department} Manager",
                "access_type": "DEPARTMENT",
                "department": department,
                "location": "ALL",
                "role_description": "Department Manager",
            }
        )

    for location in LOCATIONS:
        rows.append(
            {
                "user_email": f"manager.{location.lower()}@abcglobal.com",
                "user_name": f"{location} Location Manager",
                "access_type": "LOCATION",
                "department": "ALL",
                "location": location,
                "role_description": "Location Manager",
            }
        )

    rows.append(
        {
            "user_email": "viewer.sales.london@abcglobal.com",
            "user_name": "Sales London Viewer",
            "access_type": "RESTRICTED",
            "department": "Sales",
            "location": "London",
            "role_description": "Restricted Viewer",
        }
    )

    return pd.DataFrame(rows)


def prepare_for_csv(df: pd.DataFrame) -> pd.DataFrame:
    """Format date columns before writing CSV files."""
    output = df.copy()

    for column in output.columns:
        if pd.api.types.is_datetime64_any_dtype(output[column]):
            output[column] = output[column].dt.strftime("%Y-%m-%d")

    return output


def write_csv(df: pd.DataFrame, file_name: str) -> None:
    """Write a dataframe to the raw data folder."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / file_name
    prepare_for_csv(df).to_csv(path, index=False)


def main() -> None:
    print("Generating synthetic HR source data...")

    employees_internal = generate_employee_master()
    payroll = generate_payroll(employees_internal)
    attendance = generate_attendance(employees_internal)
    leave = generate_leave(employees_internal)
    recruitment = generate_recruitment(employees_internal)
    training = generate_training(employees_internal)
    performance = generate_performance(employees_internal)
    attrition = generate_attrition(employees_internal)
    security_mapping = generate_security_mapping()

    employee_columns = [
        "employee_id",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "hire_date",
        "department",
        "job_role",
        "job_level",
        "location",
        "country",
        "work_mode",
        "manager_id",
        "employment_type",
        "employee_status",
        "email",
    ]

    employees = employees_internal[employee_columns].copy()

    write_csv(employees, "employees.csv")
    write_csv(payroll, "payroll.csv")
    write_csv(attendance, "attendance.csv")
    write_csv(leave, "leave.csv")
    write_csv(recruitment, "recruitment.csv")
    write_csv(training, "training.csv")
    write_csv(performance, "performance.csv")
    write_csv(attrition, "attrition.csv")
    write_csv(security_mapping, "security_mapping.csv")

    outputs = {
        "employees.csv": employees,
        "payroll.csv": payroll,
        "attendance.csv": attendance,
        "leave.csv": leave,
        "recruitment.csv": recruitment,
        "training.csv": training,
        "performance.csv": performance,
        "attrition.csv": attrition,
        "security_mapping.csv": security_mapping,
    }

    print("\nSynthetic data generated successfully.")
    print(f"Output folder: {RAW_DIR}")
    print("\nRow counts:")
    for file_name, df in outputs.items():
        print(f"  {file_name:<22} {len(df):>8,} rows")


if __name__ == "__main__":
    main()
