# Power BI Model Guide  
## Enterprise Workforce Intelligence Platform

---

## 1. Purpose

This document explains how the Gold layer CSV files should be imported into Power BI Desktop and modelled for the Enterprise Workforce Intelligence Platform.

The Power BI report will use the Gold layer tables created from the Silver to Gold pipeline.

Source folder:

```text
data/gold/
```

The Power BI report file should be saved as:

```text
powerbi/reports/workforce-intelligence-report.pbix
```

---

## 2. Gold Tables to Import

Import the following CSV files into Power BI Desktop:

```text
dim_employee.csv
dim_department.csv
dim_job_role.csv
dim_location.csv
dim_date.csv
dim_manager.csv
dim_security_user.csv

fact_payroll.csv
fact_attendance.csv
fact_leave.csv
fact_recruitment.csv
fact_training.csv
fact_performance.csv
fact_attrition.csv

ml_attrition_dataset.csv
```

Do not import these into the main report model unless needed for documentation:

```text
gold_build_summary.csv
gold_relationship_validation.csv
```

These two are useful for validation, but they are not required for dashboard visuals.

---

## 3. Recommended Import Method

In Power BI Desktop:

```text
Home
  → Get Data
  → Text/CSV
```

Import each Gold CSV file one by one.

After importing, rename each table exactly as:

```text
dim_employee
dim_department
dim_job_role
dim_location
dim_date
dim_manager
dim_security_user
fact_payroll
fact_attendance
fact_leave
fact_recruitment
fact_training
fact_performance
fact_attrition
ml_attrition_dataset
```

---

## 4. Data Type Setup

After importing, check the data types in Power Query or Model View.

### 4.1 Whole Number Columns

Set these fields as Whole Number:

```text
employee_key
department_key
job_role_key
location_key
manager_key
date_key
security_user_key

payroll_key
attendance_key
leave_key
recruitment_key
training_key
performance_key
attrition_key

pay_period_key
attendance_month_key
leave_start_date_key
leave_end_date_key
application_date_key
interview_date_key
offer_date_key
hire_date_key
assigned_date_key
completion_date_key
exit_date_key

working_days
present_days
absent_days
late_arrivals
remote_work_days
review_year
performance_rating
potential_rating
promotion_flag
attrition_flag
regrettable_attrition_flag
notice_period_days
completion_flag
```

### 4.2 Decimal Number Columns

Set these fields as Decimal Number:

```text
annual_salary
monthly_salary
bonus_amount
overtime_hours
attendance_rate
absence_rate
leave_days
time_to_hire_days
training_hours
training_score
tenure_years
age
training_completion_rate
```

### 4.3 Date Columns

Set these fields as Date:

```text
dim_date[full_date]
dim_employee[date_of_birth]
dim_employee[hire_date]
dim_employee[exit_date]
```

The fact tables mainly use date keys, so they should stay as whole numbers.

---

## 5. Model Design

The model should follow a dimensional design.

Microsoft recommends star schema design principles for Power BI models because dimensions can filter fact tables efficiently. This project uses a dimensional model with employee, department, location, role, manager, and date dimensions connected to fact tables. :contentReference[oaicite:1]{index=1}

The model is a small snowflake-style variation because:

```text
dim_department
dim_job_role
dim_location
dim_manager
```

connect to:

```text
dim_employee
```

and `dim_employee` connects to employee-level fact tables.

---

## 6. Relationships to Create

Power BI may detect some relationships automatically, but check them manually. Microsoft’s guidance says relationships can be created or edited manually through Manage relationships when needed. :contentReference[oaicite:2]{index=2}

Create these relationships.

---

### 6.1 Employee Dimension Relationships

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter |
|---|---|---|---|---|---|
| dim_department | department_key | dim_employee | department_key | One-to-many | Single |
| dim_job_role | job_role_key | dim_employee | job_role_key | One-to-many | Single |
| dim_location | location_key | dim_employee | location_key | One-to-many | Single |
| dim_manager | manager_key | dim_employee | manager_key | One-to-many | Single |

---

### 6.2 Employee to Fact Relationships

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter |
|---|---|---|---|---|---|
| dim_employee | employee_key | fact_payroll | employee_key | One-to-many | Single |
| dim_employee | employee_key | fact_attendance | employee_key | One-to-many | Single |
| dim_employee | employee_key | fact_leave | employee_key | One-to-many | Single |
| dim_employee | employee_key | fact_training | employee_key | One-to-many | Single |
| dim_employee | employee_key | fact_performance | employee_key | One-to-many | Single |
| dim_employee | employee_key | fact_attrition | employee_key | One-to-many | Single |

---

### 6.3 Recruitment Fact Relationships

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter |
|---|---|---|---|---|---|
| dim_department | department_key | fact_recruitment | department_key | One-to-many | Single |
| dim_job_role | job_role_key | fact_recruitment | job_role_key | One-to-many | Single |
| dim_location | location_key | fact_recruitment | location_key | One-to-many | Single |
| dim_employee | employee_key | fact_recruitment | hired_employee_key | One-to-many | Single |

The relationship between `dim_employee` and `fact_recruitment` may contain blanks because not all candidates are hired.

---

### 6.4 Date Relationships

Create these active date relationships:

| From Table | From Column | To Table | To Column | Active? |
|---|---|---|---|---|
| dim_date | date_key | fact_payroll | pay_period_key | Yes |
| dim_date | date_key | fact_attendance | attendance_month_key | Yes |
| dim_date | date_key | fact_leave | leave_start_date_key | Yes |
| dim_date | date_key | fact_recruitment | application_date_key | Yes |
| dim_date | date_key | fact_training | assigned_date_key | Yes |
| dim_date | date_key | fact_attrition | exit_date_key | Yes |

Optional inactive relationships:

| From Table | From Column | To Table | To Column | Active? |
|---|---|---|---|---|
| dim_date | date_key | fact_leave | leave_end_date_key | No |
| dim_date | date_key | fact_recruitment | interview_date_key | No |
| dim_date | date_key | fact_recruitment | offer_date_key | No |
| dim_date | date_key | fact_recruitment | hire_date_key | No |
| dim_date | date_key | fact_training | completion_date_key | No |

Only one active relationship should exist between `dim_date` and the same fact table unless Power BI allows a clear path without ambiguity.

---

## 7. Table Visibility Recommendations

Hide technical columns from report view where appropriate.

Examples to hide:

```text
employee_key
department_key
job_role_key
location_key
manager_key
date_key
security_user_key

payroll_key
attendance_key
leave_key
recruitment_key
training_key
performance_key
attrition_key
```

Keep business-friendly fields visible:

```text
full_name
gender
age
hire_date
tenure_years
employee_status
work_mode
department_name
job_role
job_level
location
region
month_name
quarter
year
salary_band
leave_type
recruitment_source
course_category
performance_rating
exit_reason
```

---

## 8. Measures Table

Create a dedicated measures table in Power BI.

Recommended name:

```text
_Measures
```

You can create it using:

```text
Home
  → Enter Data
```

Create one dummy column with one row, then name the table `_Measures`.

After creating all measures, hide the dummy column.

---

## 9. Planned Dashboard Pages

The Power BI report should include these pages:

| Page | Purpose |
|---|---|
| Executive Overview | High-level workforce KPIs and trends |
| Workforce Demographics | Employee distribution by department, location, role, gender, and work mode |
| Attrition Analysis | Attrition rate, leavers, exit reasons, and attrition patterns |
| Recruitment Analysis | Hiring source, time to hire, offers, and hires |
| Attendance and Leave | Absence rate, leave days, and attendance trends |
| Payroll Analysis | Salary cost, average salary, salary band distribution |
| Training and Performance | Training completion, performance ratings, and promotions |
| Attrition Prediction | ML attrition dataset insights and model output later |
| RLS Testing | Simple internal page to verify visible employees by user access |

---

## 10. Power BI Service and Publishing Notes

The report will later be published from Power BI Desktop to Power BI Service.

When a Power BI Desktop file is published to Power BI Service, the semantic model and report are uploaded into the selected workspace. If the file is republished later, the semantic model and report are replaced with the updated version. :contentReference[oaicite:3]{index=3}

The project will later include:

```text
Power BI Service workspace
Published semantic model
Published report
Row-Level Security roles
RLS user assignment
RLS testing screenshots
```

---

## 11. RLS Notes

Power BI Row-Level Security restricts rows based on filters defined in roles. RLS is applied at the semantic model level and then affects report users who consume the report. :contentReference[oaicite:4]{index=4}

Important note for this project:

```text
RLS should be tested with Viewer-level users.
```

Microsoft’s documentation states that RLS applies to users with Viewer permissions in a workspace, but not to workspace Admin, Member, or Contributor roles. :contentReference[oaicite:5]{index=5}

The detailed RLS implementation will be created in a later milestone.