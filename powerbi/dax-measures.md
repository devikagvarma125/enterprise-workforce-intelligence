# Power BI DAX Measures  
## Enterprise Workforce Intelligence Platform

---

## 1. Purpose

This document contains the DAX measures used in the Power BI report for the Enterprise Workforce Intelligence Platform.

The measures are grouped by business area:

- Workforce Overview
- Attrition
- Payroll
- Attendance
- Leave
- Recruitment
- Training
- Performance
- Machine Learning Dataset
- Row-Level Security Testing

Create these measures in a dedicated Power BI measures table called:

```text
_Measures
```

---

## 2. Workforce Overview Measures

```DAX
Total Employees =
DISTINCTCOUNT(dim_employee[employee_key])
```

```DAX
Active Headcount =
CALCULATE(
    DISTINCTCOUNT(dim_employee[employee_key]),
    dim_employee[employee_status] = "Active"
)
```

```DAX
Inactive or Left Employees =
CALCULATE(
    DISTINCTCOUNT(dim_employee[employee_key]),
    dim_employee[employee_status] <> "Active"
)
```

```DAX
Average Age =
AVERAGE(dim_employee[age])
```

```DAX
Average Tenure Years =
AVERAGE(dim_employee[tenure_years])
```

```DAX
Hybrid Employees =
CALCULATE(
    [Active Headcount],
    dim_employee[work_mode] = "Hybrid"
)
```

```DAX
Remote Employees =
CALCULATE(
    [Active Headcount],
    dim_employee[work_mode] = "Remote"
)
```

```DAX
Office Employees =
CALCULATE(
    [Active Headcount],
    dim_employee[work_mode] = "Office"
)
```

```DAX
Hybrid Employee % =
DIVIDE(
    [Hybrid Employees],
    [Active Headcount]
)
```

```DAX
Remote Employee % =
DIVIDE(
    [Remote Employees],
    [Active Headcount]
)
```

```DAX
Office Employee % =
DIVIDE(
    [Office Employees],
    [Active Headcount]
)
```

---

## 3. Attrition Measures

```DAX
Leavers =
CALCULATE(
    DISTINCTCOUNT(fact_attrition[employee_key]),
    fact_attrition[attrition_flag] = 1
)
```

```DAX
Attrition Rate % =
DIVIDE(
    [Leavers],
    [Total Employees]
)
```

```DAX
Voluntary Leavers =
CALCULATE(
    [Leavers],
    fact_attrition[attrition_type] = "Voluntary"
)
```

```DAX
Involuntary Leavers =
CALCULATE(
    [Leavers],
    fact_attrition[attrition_type] = "Involuntary"
)
```

```DAX
Voluntary Attrition % =
DIVIDE(
    [Voluntary Leavers],
    [Leavers]
)
```

```DAX
Regrettable Leavers =
CALCULATE(
    [Leavers],
    fact_attrition[regrettable_attrition_flag] = 1
)
```

```DAX
Regrettable Attrition % =
DIVIDE(
    [Regrettable Leavers],
    [Leavers]
)
```

```DAX
Average Notice Period Days =
AVERAGE(fact_attrition[notice_period_days])
```

---

## 4. Payroll Measures

```DAX
Total Monthly Salary Cost =
SUM(fact_payroll[monthly_salary])
```

```DAX
Total Annual Salary Value =
SUM(fact_payroll[annual_salary])
```

```DAX
Average Annual Salary =
AVERAGE(fact_payroll[annual_salary])
```

```DAX
Average Monthly Salary =
AVERAGE(fact_payroll[monthly_salary])
```

```DAX
Total Bonus Amount =
SUM(fact_payroll[bonus_amount])
```

```DAX
Paid Employees =
DISTINCTCOUNT(fact_payroll[employee_key])
```

```DAX
Average Bonus Amount =
AVERAGE(fact_payroll[bonus_amount])
```

```DAX
Salary Cost per Employee =
DIVIDE(
    [Total Monthly Salary Cost],
    [Paid Employees]
)
```

---

## 5. Attendance Measures

```DAX
Total Working Days =
SUM(fact_attendance[working_days])
```

```DAX
Total Present Days =
SUM(fact_attendance[present_days])
```

```DAX
Total Absent Days =
SUM(fact_attendance[absent_days])
```

```DAX
Total Late Arrivals =
SUM(fact_attendance[late_arrivals])
```

```DAX
Total Remote Work Days =
SUM(fact_attendance[remote_work_days])
```

```DAX
Total Overtime Hours =
SUM(fact_attendance[overtime_hours])
```

```DAX
Attendance Rate % =
DIVIDE(
    [Total Present Days],
    [Total Working Days]
)
```

```DAX
Absence Rate % =
DIVIDE(
    [Total Absent Days],
    [Total Working Days]
)
```

```DAX
Average Late Arrivals =
AVERAGE(fact_attendance[late_arrivals])
```

```DAX
Average Overtime Hours =
AVERAGE(fact_attendance[overtime_hours])
```

---

## 6. Leave Measures

```DAX
Leave Records =
COUNTROWS(fact_leave)
```

```DAX
Total Leave Days =
SUM(fact_leave[leave_days])
```

```DAX
Approved Leave Days =
CALCULATE(
    [Total Leave Days],
    fact_leave[leave_status] = "Approved"
)
```

```DAX
Rejected Leave Days =
CALCULATE(
    [Total Leave Days],
    fact_leave[leave_status] = "Rejected"
)
```

```DAX
Pending Leave Days =
CALCULATE(
    [Total Leave Days],
    fact_leave[leave_status] = "Pending"
)
```

```DAX
Average Leave Days =
AVERAGE(fact_leave[leave_days])
```

```DAX
Sick Leave Days =
CALCULATE(
    [Total Leave Days],
    fact_leave[leave_type] = "Sick"
)
```

```DAX
Annual Leave Days =
CALCULATE(
    [Total Leave Days],
    fact_leave[leave_type] = "Annual"
)
```

---

## 7. Recruitment Measures

```DAX
Total Candidates =
DISTINCTCOUNT(fact_recruitment[candidate_id])
```

```DAX
Hired Candidates =
CALCULATE(
    [Total Candidates],
    fact_recruitment[status] = "Hired"
)
```

```DAX
Offered Candidates =
CALCULATE(
    [Total Candidates],
    fact_recruitment[status] = "Offered"
)
```

```DAX
Rejected Candidates =
CALCULATE(
    [Total Candidates],
    fact_recruitment[status] = "Rejected"
)
```

```DAX
Hire Rate % =
DIVIDE(
    [Hired Candidates],
    [Total Candidates]
)
```

```DAX
Average Time to Hire Days =
AVERAGE(fact_recruitment[time_to_hire_days])
```

```DAX
Open or In Progress Candidates =
CALCULATE(
    [Total Candidates],
    fact_recruitment[status] IN { "Applied", "Interviewed", "Offered" }
)
```

```DAX
Offer to Hire Conversion % =
DIVIDE(
    [Hired Candidates],
    [Offered Candidates] + [Hired Candidates]
)
```

---

## 8. Training Measures

```DAX
Training Records =
COUNTROWS(fact_training)
```

```DAX
Completed Training Records =
CALCULATE(
    COUNTROWS(fact_training),
    fact_training[completion_flag] = 1
)
```

```DAX
Training Completion Rate % =
DIVIDE(
    [Completed Training Records],
    [Training Records]
)
```

```DAX
Total Training Hours =
SUM(fact_training[training_hours])
```

```DAX
Average Training Hours =
AVERAGE(fact_training[training_hours])
```

```DAX
Average Training Score =
AVERAGE(fact_training[training_score])
```

```DAX
Overdue Training Records =
CALCULATE(
    COUNTROWS(fact_training),
    fact_training[completion_status] = "Overdue"
)
```

```DAX
Training Overdue Rate % =
DIVIDE(
    [Overdue Training Records],
    [Training Records]
)
```

---

## 9. Performance Measures

```DAX
Performance Review Count =
COUNTROWS(fact_performance)
```

```DAX
Average Performance Rating =
AVERAGE(fact_performance[performance_rating])
```

```DAX
Average Potential Rating =
AVERAGE(fact_performance[potential_rating])
```

```DAX
Promotions =
CALCULATE(
    COUNTROWS(fact_performance),
    fact_performance[promotion_flag] = 1
)
```

```DAX
Promotion Rate % =
DIVIDE(
    [Promotions],
    [Performance Review Count]
)
```

```DAX
High Performers =
CALCULATE(
    DISTINCTCOUNT(fact_performance[employee_key]),
    fact_performance[performance_rating] >= 4
)
```

```DAX
Low Performers =
CALCULATE(
    DISTINCTCOUNT(fact_performance[employee_key]),
    fact_performance[performance_rating] <= 2
)
```

```DAX
High Performer % =
DIVIDE(
    [High Performers],
    DISTINCTCOUNT(fact_performance[employee_key])
)
```

---

## 10. ML Attrition Dataset Measures

These measures use the `ml_attrition_dataset` table.

```DAX
ML Employee Count =
COUNTROWS(ml_attrition_dataset)
```

```DAX
ML Leavers =
CALCULATE(
    COUNTROWS(ml_attrition_dataset),
    ml_attrition_dataset[attrition_flag] = 1
)
```

```DAX
ML Attrition Rate % =
DIVIDE(
    [ML Leavers],
    [ML Employee Count]
)
```

```DAX
ML Average Age =
AVERAGE(ml_attrition_dataset[age])
```

```DAX
ML Average Tenure =
AVERAGE(ml_attrition_dataset[tenure_years])
```

```DAX
ML Average Salary =
AVERAGE(ml_attrition_dataset[annual_salary])
```

```DAX
ML Average Absence Rate % =
AVERAGE(ml_attrition_dataset[absence_rate])
```

```DAX
ML Average Training Hours =
AVERAGE(ml_attrition_dataset[training_hours])
```

```DAX
ML Average Performance Rating =
AVERAGE(ml_attrition_dataset[performance_rating])
```

---

## 11. RLS Testing Measures

These measures will help test Row-Level Security later.

```DAX
Current Power BI User =
USERPRINCIPALNAME()
```

```DAX
Visible Employees =
DISTINCTCOUNT(dim_employee[employee_key])
```

```DAX
Visible Departments =
DISTINCTCOUNT(dim_department[department_name])
```

```DAX
Visible Locations =
DISTINCTCOUNT(dim_location[location])
```

```DAX
Visible Salary Cost =
[Total Monthly Salary Cost]
```

```DAX
Visible Leavers =
[Leavers]
```

---

## 12. Formatting Recommendations

Format these measures as Percentage:

```text
Hybrid Employee %
Remote Employee %
Office Employee %
Attrition Rate %
Voluntary Attrition %
Regrettable Attrition %
Attendance Rate %
Absence Rate %
Hire Rate %
Offer to Hire Conversion %
Training Completion Rate %
Training Overdue Rate %
Promotion Rate %
High Performer %
ML Attrition Rate %
ML Average Absence Rate %
```

Format these measures as Currency:

```text
Total Monthly Salary Cost
Total Annual Salary Value
Average Annual Salary
Average Monthly Salary
Total Bonus Amount
Average Bonus Amount
Salary Cost per Employee
ML Average Salary
Visible Salary Cost
```

Format these measures as Whole Number:

```text
Total Employees
Active Headcount
Leavers
Paid Employees
Total Candidates
Hired Candidates
Training Records
Performance Review Count
Promotions
Visible Employees
Visible Departments
Visible Locations
```

---

## 13. Notes

- Measures should be created in the `_Measures` table.
- Technical keys should be hidden from report view after relationships are created.
- The `ml_attrition_dataset` measures are for analysis and portfolio demonstration.
- RLS measures will be used later when Row-Level Security is implemented.
- Some measures may be refined after the dashboard layout is created.