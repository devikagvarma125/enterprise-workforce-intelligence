-- Workforce Analytics SQL Queries
-- Enterprise Workforce Intelligence Platform


-- name: 01_active_headcount_by_department_location
SELECT
    d.department_name,
    l.location,
    COUNT(e.employee_key) AS active_headcount
FROM dim_employee e
INNER JOIN dim_department d
    ON e.department_key = d.department_key
INNER JOIN dim_location l
    ON e.location_key = l.location_key
WHERE e.employee_status = 'Active'
GROUP BY
    d.department_name,
    l.location
ORDER BY
    active_headcount DESC;


-- name: 02_headcount_by_work_mode
SELECT
    e.work_mode,
    COUNT(e.employee_key) AS employee_count,
    ROUND(
        COUNT(e.employee_key) * 100.0 /
        (SELECT COUNT(*) FROM dim_employee WHERE employee_status = 'Active'),
        2
    ) AS employee_percentage
FROM dim_employee e
WHERE e.employee_status = 'Active'
GROUP BY
    e.work_mode
ORDER BY
    employee_count DESC;


-- name: 03_attrition_rate_by_department
WITH leavers AS (
    SELECT DISTINCT
        employee_key
    FROM fact_attrition
    WHERE attrition_flag = 1
)
SELECT
    d.department_name,
    COUNT(e.employee_key) AS total_employees,
    SUM(CASE WHEN l.employee_key IS NOT NULL THEN 1 ELSE 0 END) AS leavers,
    ROUND(
        SUM(CASE WHEN l.employee_key IS NOT NULL THEN 1 ELSE 0 END) * 100.0
        / COUNT(e.employee_key),
        2
    ) AS attrition_rate_percentage
FROM dim_employee e
INNER JOIN dim_department d
    ON e.department_key = d.department_key
LEFT JOIN leavers l
    ON e.employee_key = l.employee_key
GROUP BY
    d.department_name
ORDER BY
    attrition_rate_percentage DESC;


-- name: 04_attrition_rate_by_location
WITH leavers AS (
    SELECT DISTINCT
        employee_key
    FROM fact_attrition
    WHERE attrition_flag = 1
)
SELECT
    l.location,
    COUNT(e.employee_key) AS total_employees,
    SUM(CASE WHEN a.employee_key IS NOT NULL THEN 1 ELSE 0 END) AS leavers,
    ROUND(
        SUM(CASE WHEN a.employee_key IS NOT NULL THEN 1 ELSE 0 END) * 100.0
        / COUNT(e.employee_key),
        2
    ) AS attrition_rate_percentage
FROM dim_employee e
INNER JOIN dim_location l
    ON e.location_key = l.location_key
LEFT JOIN leavers a
    ON e.employee_key = a.employee_key
GROUP BY
    l.location
ORDER BY
    attrition_rate_percentage DESC;


-- name: 05_monthly_salary_cost_by_department
SELECT
    dt.year,
    dt.month,
    dt.month_name,
    d.department_name,
    ROUND(SUM(p.monthly_salary), 2) AS total_monthly_salary_cost,
    ROUND(AVG(p.annual_salary), 2) AS average_annual_salary,
    COUNT(DISTINCT p.employee_key) AS paid_employees
FROM fact_payroll p
INNER JOIN dim_employee e
    ON p.employee_key = e.employee_key
INNER JOIN dim_department d
    ON e.department_key = d.department_key
INNER JOIN dim_date dt
    ON p.pay_period_key = dt.date_key
GROUP BY
    dt.year,
    dt.month,
    dt.month_name,
    d.department_name
ORDER BY
    dt.year,
    dt.month,
    total_monthly_salary_cost DESC;


-- name: 06_latest_salary_band_distribution
WITH latest_payroll AS (
    SELECT
        employee_key,
        MAX(pay_period_key) AS latest_pay_period_key
    FROM fact_payroll
    GROUP BY
        employee_key
)
SELECT
    p.salary_band,
    COUNT(DISTINCT p.employee_key) AS employee_count,
    ROUND(AVG(p.annual_salary), 2) AS average_annual_salary
FROM fact_payroll p
INNER JOIN latest_payroll lp
    ON p.employee_key = lp.employee_key
    AND p.pay_period_key = lp.latest_pay_period_key
GROUP BY
    p.salary_band,
    p.salary_band_sort_order
ORDER BY
    p.salary_band_sort_order;


-- name: 07_absence_rate_by_department_month
SELECT
    dt.year,
    dt.month,
    dt.month_name,
    d.department_name,
    ROUND(AVG(a.absence_rate) * 100, 2) AS average_absence_rate_percentage,
    SUM(a.absent_days) AS total_absent_days,
    SUM(a.working_days) AS total_working_days
FROM fact_attendance a
INNER JOIN dim_employee e
    ON a.employee_key = e.employee_key
INNER JOIN dim_department d
    ON e.department_key = d.department_key
INNER JOIN dim_date dt
    ON a.attendance_month_key = dt.date_key
GROUP BY
    dt.year,
    dt.month,
    dt.month_name,
    d.department_name
ORDER BY
    dt.year,
    dt.month,
    average_absence_rate_percentage DESC;


-- name: 08_recruitment_source_effectiveness
SELECT
    recruitment_source,
    COUNT(candidate_id) AS total_candidates,
    SUM(CASE WHEN status = 'Hired' THEN 1 ELSE 0 END) AS hired_candidates,
    ROUND(
        SUM(CASE WHEN status = 'Hired' THEN 1 ELSE 0 END) * 100.0
        / COUNT(candidate_id),
        2
    ) AS hire_rate_percentage,
    ROUND(
        AVG(CASE WHEN status = 'Hired' THEN time_to_hire_days ELSE NULL END),
        2
    ) AS average_time_to_hire_days
FROM fact_recruitment
GROUP BY
    recruitment_source
ORDER BY
    hired_candidates DESC;


-- name: 09_training_completion_by_department
SELECT
    d.department_name,
    COUNT(t.training_key) AS training_records,
    SUM(CASE WHEN t.completion_flag = 1 THEN 1 ELSE 0 END) AS completed_training_records,
    ROUND(AVG(t.completion_flag) * 100, 2) AS completion_rate_percentage,
    ROUND(SUM(t.training_hours), 2) AS total_training_hours,
    ROUND(AVG(t.training_score), 2) AS average_training_score
FROM fact_training t
INNER JOIN dim_employee e
    ON t.employee_key = e.employee_key
INNER JOIN dim_department d
    ON e.department_key = d.department_key
GROUP BY
    d.department_name
ORDER BY
    completion_rate_percentage DESC;


-- name: 10_performance_rating_distribution_by_department
SELECT
    d.department_name,
    p.performance_rating,
    COUNT(p.performance_key) AS review_count,
    ROUND(AVG(p.potential_rating), 2) AS average_potential_rating,
    SUM(CASE WHEN p.promotion_flag = 1 THEN 1 ELSE 0 END) AS promotions
FROM fact_performance p
INNER JOIN dim_employee e
    ON p.employee_key = e.employee_key
INNER JOIN dim_department d
    ON e.department_key = d.department_key
GROUP BY
    d.department_name,
    p.performance_rating
ORDER BY
    d.department_name,
    p.performance_rating;


-- name: 11_leave_days_by_type
SELECT
    leave_type,
    leave_status,
    COUNT(leave_key) AS leave_records,
    SUM(leave_days) AS total_leave_days,
    ROUND(AVG(leave_days), 2) AS average_leave_days
FROM fact_leave
GROUP BY
    leave_type,
    leave_status
ORDER BY
    total_leave_days DESC;


-- name: 12_attrition_feature_summary
SELECT
    attrition_flag,
    COUNT(*) AS employee_count,
    ROUND(AVG(age), 2) AS average_age,
    ROUND(AVG(tenure_years), 2) AS average_tenure_years,
    ROUND(AVG(annual_salary), 2) AS average_annual_salary,
    ROUND(AVG(absence_rate) * 100, 2) AS average_absence_rate_percentage,
    ROUND(AVG(late_arrivals), 2) AS average_late_arrivals,
    ROUND(AVG(training_hours), 2) AS average_training_hours,
    ROUND(AVG(training_completion_rate) * 100, 2) AS average_training_completion_percentage,
    ROUND(AVG(performance_rating), 2) AS average_performance_rating
FROM ml_attrition_dataset
GROUP BY
    attrition_flag
ORDER BY
    attrition_flag;


-- name: 13_rls_access_preview
SELECT
    s.user_email,
    s.role_description,
    s.access_type,
    s.department AS security_department,
    s.location AS security_location,
    COUNT(DISTINCT e.employee_key) AS visible_employee_count
FROM dim_security_user s
CROSS JOIN dim_employee e
INNER JOIN dim_department d
    ON e.department_key = d.department_key
INNER JOIN dim_location l
    ON e.location_key = l.location_key
WHERE
    s.access_type = 'ALL'
    OR (
        s.access_type = 'DEPARTMENT'
        AND d.department_name = s.department
    )
    OR (
        s.access_type = 'LOCATION'
        AND l.location = s.location
    )
    OR (
        s.access_type = 'RESTRICTED'
        AND (s.department = 'ALL' OR d.department_name = s.department)
        AND (s.location = 'ALL' OR l.location = s.location)
    )
GROUP BY
    s.user_email,
    s.role_description,
    s.access_type,
    s.department,
    s.location
ORDER BY
    visible_employee_count DESC;