# Source-to-Target Mapping  
## Enterprise Workforce Intelligence Platform

---

## 1. Purpose of This Document

This document defines how source HR datasets will be transformed into reporting-ready Gold layer tables for the Enterprise Workforce Intelligence Platform.

It explains:

- Source files used in the project.
- Key fields in each source file.
- Raw, Bronze, Silver, and Gold layer mapping.
- Target dimension and fact tables.
- Transformation rules.
- Data quality checks.
- Row-Level Security mapping design.

This document will guide the Python scripts, Databricks notebooks, SQL queries, Power BI model, and dashboard development.

---

## 2. Data Layer Overview

The project follows a Lakehouse-style medallion architecture.

```text
Source Files
    ↓
Raw Layer
    ↓
Bronze Layer
    ↓
Silver Layer
    ↓
Gold Layer
    ↓
Power BI Report
    ↓
Power BI Service with RLS
```

---

## 3. Source Data Files

The project will use synthetic HR source files.

| Source File | Business Area | Description |
|---|---|---|
| employees.csv | Employee Master | Stores employee profile, department, role, location, manager, hire date, and employment status |
| payroll.csv | Payroll | Stores salary, bonus, pay grade, and salary band information |
| attendance.csv | Attendance | Stores monthly attendance, absence, late arrivals, and working day information |
| leave.csv | Leave Management | Stores employee leave records by leave type and date range |
| recruitment.csv | Recruitment | Stores candidate, vacancy, hiring source, application, offer, and hire information |
| training.csv | Training | Stores employee training records, completion status, and training hours |
| performance.csv | Performance | Stores employee review ratings, review period, and promotion information |
| attrition.csv | Attrition | Stores employee exit date, exit reason, and leaver type |
| security_mapping.csv | Security / RLS | Stores user access rules for Power BI Row-Level Security |

---

## 4. Source File Schemas

---

### 4.1 employees.csv

| Column | Description |
|---|---|
| employee_id | Unique employee identifier |
| first_name | Employee first name |
| last_name | Employee last name |
| gender | Employee gender |
| date_of_birth | Employee date of birth |
| hire_date | Employee hire date |
| department | Department name |
| job_role | Employee job role |
| job_level | Employee seniority level |
| location | Office location |
| country | Country |
| work_mode | Office, Hybrid, or Remote |
| manager_id | Employee's manager ID |
| employment_type | Full-time, Part-time, or Contract |
| employee_status | Active or Left |
| email | Synthetic employee email address |

---

### 4.2 payroll.csv

| Column | Description |
|---|---|
| payroll_id | Unique payroll record identifier |
| employee_id | Employee identifier |
| pay_period | Payroll month |
| annual_salary | Annual salary amount |
| monthly_salary | Monthly salary amount |
| bonus_amount | Bonus amount for the pay period |
| pay_grade | Pay grade |
| salary_band | Salary band |
| currency | Payroll currency |

---

### 4.3 attendance.csv

| Column | Description |
|---|---|
| attendance_id | Unique attendance record identifier |
| employee_id | Employee identifier |
| attendance_month | Attendance reporting month |
| working_days | Number of working days in the month |
| present_days | Number of days employee was present |
| absent_days | Number of days employee was absent |
| late_arrivals | Number of late arrivals |
| remote_work_days | Number of remote work days |
| overtime_hours | Overtime hours worked |

---

### 4.4 leave.csv

| Column | Description |
|---|---|
| leave_id | Unique leave record identifier |
| employee_id | Employee identifier |
| leave_type | Annual, Sick, Unpaid, Maternity, Paternity, or Other |
| leave_start_date | Leave start date |
| leave_end_date | Leave end date |
| leave_days | Number of leave days |
| leave_status | Approved, Rejected, or Pending |

---

### 4.5 recruitment.csv

| Column | Description |
|---|---|
| candidate_id | Unique candidate identifier |
| requisition_id | Hiring requisition identifier |
| department | Hiring department |
| job_role | Hiring job role |
| location | Hiring location |
| recruitment_source | Job Board, Referral, LinkedIn, Agency, Campus, or Company Website |
| application_date | Candidate application date |
| interview_date | Candidate interview date |
| offer_date | Offer date |
| hire_date | Hire date |
| status | Applied, Interviewed, Offered, Hired, or Rejected |
| hired_employee_id | Employee ID if the candidate was hired |
| time_to_hire_days | Number of days from application to hire |

---

### 4.6 training.csv

| Column | Description |
|---|---|
| training_id | Unique training record identifier |
| employee_id | Employee identifier |
| course_name | Training course name |
| course_category | Technical, Compliance, Leadership, HR, Finance, or Soft Skills |
| assigned_date | Training assigned date |
| completion_date | Training completion date |
| completion_status | Completed, In Progress, Not Started, or Overdue |
| training_hours | Training duration in hours |
| training_score | Training score or assessment result |

---

### 4.7 performance.csv

| Column | Description |
|---|---|
| performance_id | Unique performance review identifier |
| employee_id | Employee identifier |
| review_year | Review year |
| review_period | Annual, Mid-Year, or Quarterly |
| performance_rating | Performance rating from 1 to 5 |
| potential_rating | Potential rating from 1 to 5 |
| promotion_flag | Whether the employee was promoted |
| manager_id | Reviewing manager ID |

---

### 4.8 attrition.csv

| Column | Description |
|---|---|
| attrition_id | Unique attrition record identifier |
| employee_id | Employee identifier |
| exit_date | Employee exit date |
| exit_reason | Resignation, Better Opportunity, Retirement, Termination, Relocation, Personal Reasons, or Other |
| attrition_type | Voluntary or Involuntary |
| regrettable_attrition_flag | Whether the attrition was regrettable |
| notice_period_days | Number of notice period days |

---

### 4.9 security_mapping.csv

| Column | Description |
|---|---|
| user_email | Power BI user email |
| user_name | User display name |
| access_type | ALL, DEPARTMENT, LOCATION, or RESTRICTED |
| department | Department user is allowed to view |
| location | Location user is allowed to view |
| role_description | HR Director, Department Manager, Location Manager, or Viewer |

---

## 5. Raw to Bronze Mapping

The Raw layer stores source files exactly as generated.

The Bronze layer standardises the raw files but does not apply major business transformations.

| Raw Source | Bronze Target | Transformation |
|---|---|---|
| employees.csv | bronze_employees | Standardise column names, add ingestion timestamp, add source file name |
| payroll.csv | bronze_payroll | Standardise column names, add ingestion timestamp, add source file name |
| attendance.csv | bronze_attendance | Standardise column names, add ingestion timestamp, add source file name |
| leave.csv | bronze_leave | Standardise column names, add ingestion timestamp, add source file name |
| recruitment.csv | bronze_recruitment | Standardise column names, add ingestion timestamp, add source file name |
| training.csv | bronze_training | Standardise column names, add ingestion timestamp, add source file name |
| performance.csv | bronze_performance | Standardise column names, add ingestion timestamp, add source file name |
| attrition.csv | bronze_attrition | Standardise column names, add ingestion timestamp, add source file name |
| security_mapping.csv | bronze_security_mapping | Standardise column names, add ingestion timestamp, add source file name |

---

## 6. Bronze to Silver Mapping

The Silver layer applies cleaning, validation, and business rules.

| Bronze Table | Silver Target | Main Transformations |
|---|---|---|
| bronze_employees | silver_employees | Remove duplicates, validate employee IDs, standardise department/location/role, create full name, calculate age and tenure |
| bronze_payroll | silver_payroll | Validate salary values, standardise pay period, calculate monthly salary if missing |
| bronze_attendance | silver_attendance | Validate working days, calculate attendance rate and absence rate |
| bronze_leave | silver_leave | Validate leave dates, calculate leave days if missing, standardise leave type |
| bronze_recruitment | silver_recruitment | Validate application, offer and hire dates, calculate time to hire |
| bronze_training | silver_training | Validate completion status, standardise course categories, calculate completion flag |
| bronze_performance | silver_performance | Validate rating values, standardise review period, convert promotion flag |
| bronze_attrition | silver_attrition | Validate exit dates, standardise exit reasons, convert voluntary and regrettable flags |
| bronze_security_mapping | silver_security_mapping | Validate user emails, standardise access types, validate department and location values |

---

## 7. Silver to Gold Mapping

The Gold layer creates dimensional tables, fact tables, reporting views, and ML-ready datasets.

| Silver Source | Gold Target | Description |
|---|---|---|
| silver_employees | dim_employee | Employee profile dimension |
| silver_employees | dim_department | Department dimension |
| silver_employees | dim_job_role | Job role dimension |
| silver_employees | dim_location | Location dimension |
| silver_employees | dim_manager | Manager dimension |
| silver_payroll | fact_payroll | Payroll fact table |
| silver_attendance | fact_attendance | Attendance fact table |
| silver_leave | fact_leave | Leave fact table |
| silver_recruitment | fact_recruitment | Recruitment fact table |
| silver_training | fact_training | Training fact table |
| silver_performance | fact_performance | Performance fact table |
| silver_attrition | fact_attrition | Attrition fact table |
| silver_security_mapping | dim_security_user | Power BI RLS user access dimension |
| Multiple silver tables | ml_attrition_dataset | Machine learning dataset for attrition prediction |

---

## 8. Gold Dimension Tables

---

### 8.1 dim_employee

| Target Column | Source Column / Logic |
|---|---|
| employee_key | Generated surrogate key |
| employee_id | employees.employee_id |
| full_name | first_name + last_name |
| gender | employees.gender |
| date_of_birth | employees.date_of_birth |
| age | Calculated from date_of_birth |
| hire_date | employees.hire_date |
| tenure_years | Calculated from hire_date |
| employee_status | employees.employee_status |
| employment_type | employees.employment_type |
| work_mode | employees.work_mode |
| department_key | Lookup from dim_department |
| job_role_key | Lookup from dim_job_role |
| location_key | Lookup from dim_location |
| manager_key | Lookup from dim_manager |
| email | employees.email |

---

### 8.2 dim_department

| Target Column | Source Column / Logic |
|---|---|
| department_key | Generated surrogate key |
| department_name | Distinct department from employees |
| department_group | Derived business grouping |

---

### 8.3 dim_job_role

| Target Column | Source Column / Logic |
|---|---|
| job_role_key | Generated surrogate key |
| job_role | Distinct job_role from employees |
| job_level | employees.job_level |
| job_family | Derived from job role |

---

### 8.4 dim_location

| Target Column | Source Column / Logic |
|---|---|
| location_key | Generated surrogate key |
| location | Distinct location from employees |
| country | employees.country |
| region | Derived from location |

---

### 8.5 dim_manager

| Target Column | Source Column / Logic |
|---|---|
| manager_key | Generated surrogate key |
| manager_id | employees.manager_id |
| manager_name | Derived from employee record where employee_id = manager_id |
| manager_department | Manager department |

---

### 8.6 dim_date

| Target Column | Source Column / Logic |
|---|---|
| date_key | Date formatted as YYYYMMDD |
| full_date | Calendar date |
| day | Day of month |
| month | Month number |
| month_name | Month name |
| quarter | Quarter |
| year | Year |
| week_of_year | Week number |
| is_weekend | Weekend flag |

---

### 8.7 dim_security_user

| Target Column | Source Column / Logic |
|---|---|
| security_user_key | Generated surrogate key |
| user_email | security_mapping.user_email |
| user_name | security_mapping.user_name |
| access_type | security_mapping.access_type |
| department | security_mapping.department |
| location | security_mapping.location |
| role_description | security_mapping.role_description |

---

## 9. Gold Fact Tables

---

### 9.1 fact_payroll

| Target Column | Source Column / Logic |
|---|---|
| payroll_key | Generated surrogate key |
| employee_key | Lookup from dim_employee |
| pay_period_key | Lookup from dim_date |
| annual_salary | payroll.annual_salary |
| monthly_salary | payroll.monthly_salary |
| bonus_amount | payroll.bonus_amount |
| pay_grade | payroll.pay_grade |
| salary_band | payroll.salary_band |
| currency | payroll.currency |

---

### 9.2 fact_attendance

| Target Column | Source Column / Logic |
|---|---|
| attendance_key | Generated surrogate key |
| employee_key | Lookup from dim_employee |
| attendance_month_key | Lookup from dim_date |
| working_days | attendance.working_days |
| present_days | attendance.present_days |
| absent_days | attendance.absent_days |
| late_arrivals | attendance.late_arrivals |
| remote_work_days | attendance.remote_work_days |
| overtime_hours | attendance.overtime_hours |
| attendance_rate | present_days / working_days |
| absence_rate | absent_days / working_days |

---

### 9.3 fact_leave

| Target Column | Source Column / Logic |
|---|---|
| leave_key | Generated surrogate key |
| employee_key | Lookup from dim_employee |
| leave_start_date_key | Lookup from dim_date |
| leave_end_date_key | Lookup from dim_date |
| leave_type | leave.leave_type |
| leave_days | leave.leave_days |
| leave_status | leave.leave_status |

---

### 9.4 fact_recruitment

| Target Column | Source Column / Logic |
|---|---|
| recruitment_key | Generated surrogate key |
| candidate_id | recruitment.candidate_id |
| requisition_id | recruitment.requisition_id |
| department_key | Lookup from dim_department |
| job_role_key | Lookup from dim_job_role |
| location_key | Lookup from dim_location |
| application_date_key | Lookup from dim_date |
| interview_date_key | Lookup from dim_date |
| offer_date_key | Lookup from dim_date |
| hire_date_key | Lookup from dim_date |
| recruitment_source | recruitment.recruitment_source |
| status | recruitment.status |
| hired_employee_key | Lookup from dim_employee if hired |
| time_to_hire_days | recruitment.time_to_hire_days |

---

### 9.5 fact_training

| Target Column | Source Column / Logic |
|---|---|
| training_key | Generated surrogate key |
| employee_key | Lookup from dim_employee |
| assigned_date_key | Lookup from dim_date |
| completion_date_key | Lookup from dim_date |
| course_name | training.course_name |
| course_category | training.course_category |
| completion_status | training.completion_status |
| completion_flag | 1 if completed, otherwise 0 |
| training_hours | training.training_hours |
| training_score | training.training_score |

---

### 9.6 fact_performance

| Target Column | Source Column / Logic |
|---|---|
| performance_key | Generated surrogate key |
| employee_key | Lookup from dim_employee |
| review_year | performance.review_year |
| review_period | performance.review_period |
| performance_rating | performance.performance_rating |
| potential_rating | performance.potential_rating |
| promotion_flag | performance.promotion_flag |
| manager_key | Lookup from dim_manager |

---

### 9.7 fact_attrition

| Target Column | Source Column / Logic |
|---|---|
| attrition_key | Generated surrogate key |
| employee_key | Lookup from dim_employee |
| exit_date_key | Lookup from dim_date |
| exit_reason | attrition.exit_reason |
| attrition_type | attrition.attrition_type |
| attrition_flag | 1 for leaver, 0 otherwise |
| regrettable_attrition_flag | attrition.regrettable_attrition_flag |
| notice_period_days | attrition.notice_period_days |

---

## 10. ML Attrition Dataset

The machine learning dataset will combine selected fields from Gold dimension and fact tables.

Target output:

```text
ml_attrition_dataset
```

Example fields:

| Column | Source / Logic |
|---|---|
| employee_id | dim_employee.employee_id |
| age | dim_employee.age |
| gender | dim_employee.gender |
| department | dim_department.department_name |
| job_role | dim_job_role.job_role |
| job_level | dim_job_role.job_level |
| location | dim_location.location |
| work_mode | dim_employee.work_mode |
| tenure_years | dim_employee.tenure_years |
| annual_salary | fact_payroll.annual_salary |
| salary_band | fact_payroll.salary_band |
| absence_rate | fact_attendance.absence_rate |
| late_arrivals | fact_attendance.late_arrivals |
| training_hours | fact_training.training_hours |
| training_completion_flag | fact_training.completion_flag |
| performance_rating | fact_performance.performance_rating |
| promotion_flag | fact_performance.promotion_flag |
| attrition_flag | fact_attrition.attrition_flag |

---

## 11. Row-Level Security Mapping Design

Power BI Row-Level Security will use the security mapping data to restrict report visibility.

The source file is:

```text
security_mapping.csv
```

The Gold table is:

```text
dim_security_user
```

The security logic will use the logged-in Power BI user email.

Example Power BI RLS concept:

```DAX
[User Email] = USERPRINCIPALNAME()
```

---

### 11.1 Example Access Rules

| User Email | Access Type | Department | Location | Expected Report Access |
|---|---|---|---|---|
| hr.director@abcglobal.com | ALL | ALL | ALL | Can view all data |
| manager.sales@abcglobal.com | DEPARTMENT | Sales | ALL | Can view Sales department only |
| manager.finance@abcglobal.com | DEPARTMENT | Finance | ALL | Can view Finance department only |
| manager.london@abcglobal.com | LOCATION | ALL | London | Can view London location only |
| manager.manchester@abcglobal.com | LOCATION | ALL | Manchester | Can view Manchester location only |

---

## 12. Data Quality Rules

The project will apply the following validation rules.

| Rule ID | Rule |
|---|---|
| DQ-001 | Employee ID must not be null |
| DQ-002 | Employee ID must be unique in employee master data |
| DQ-003 | Hire date must not be in the future |
| DQ-004 | Exit date must not be earlier than hire date |
| DQ-005 | Department must not be blank |
| DQ-006 | Location must not be blank |
| DQ-007 | Annual salary must be greater than zero |
| DQ-008 | Working days must be greater than or equal to present days plus absent days |
| DQ-009 | Performance rating must be between 1 and 5 |
| DQ-010 | Training completion status must use approved values |
| DQ-011 | Fact records must have matching employee records |
| DQ-012 | Security mapping must contain valid user email values |

---

## 13. Naming Standards

The project will use the following naming standards.

| Object Type | Naming Standard | Example |
|---|---|---|
| Raw file | lowercase plural name | employees.csv |
| Bronze table | bronze_table_name | bronze_employees |
| Silver table | silver_table_name | silver_employees |
| Gold dimension | dim_table_name | dim_employee |
| Gold fact | fact_table_name | fact_payroll |
| Date key | YYYYMMDD integer format | 20260131 |
| Surrogate key | table_name_key | employee_key |
| Boolean flag | field_name_flag | promotion_flag |
| DAX measure | Business-friendly name | Total Headcount |

---

## 14. Expected Power BI Model

The Power BI model will use the Gold tables.

Expected relationship pattern:

```text
dim_employee      → fact_payroll
dim_employee      → fact_attendance
dim_employee      → fact_leave
dim_employee      → fact_training
dim_employee      → fact_performance
dim_employee      → fact_attrition

dim_department    → dim_employee
dim_job_role      → dim_employee
dim_location      → dim_employee
dim_manager       → dim_employee

dim_date          → fact_payroll
dim_date          → fact_attendance
dim_date          → fact_leave
dim_date          → fact_recruitment
dim_date          → fact_training
dim_date          → fact_attrition

dim_security_user → RLS filtering logic
```

---

## 15. Notes for Implementation

During implementation:

- Source files will first be generated locally using Python.
- The same files can be uploaded to Azure Data Lake Storage Gen2.
- Databricks notebooks will use the Raw layer as input.
- Bronze, Silver, and Gold outputs will be created step by step.
- Power BI will connect to Gold layer outputs.
- RLS will be tested using sample user emails.
- No real personal employee data will be used.
- Credentials and secrets must not be stored in GitHub.

---

## 16. Next Step

After this document is approved, the next project deliverables are:

1. Data Dictionary.
2. Synthetic Data Generation script.
3. Raw source datasets.
4. Databricks notebook design.
5. Power BI data model design.