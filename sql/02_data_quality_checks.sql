-- Gold Layer Data Quality Checks
-- Enterprise Workforce Intelligence Platform


-- name: 01_gold_data_quality_summary
SELECT
    check_name,
    issue_count,
    CASE
        WHEN issue_count = 0 THEN 'Pass'
        ELSE 'Review'
    END AS status
FROM (
    SELECT
        'DQ-001 Duplicate employee_id in dim_employee' AS check_name,
        COUNT(*) AS issue_count
    FROM (
        SELECT
            employee_id
        FROM dim_employee
        GROUP BY
            employee_id
        HAVING COUNT(*) > 1
    )

    UNION ALL

    SELECT
        'DQ-002 Missing employee_id in dim_employee' AS check_name,
        COUNT(*) AS issue_count
    FROM dim_employee
    WHERE employee_id IS NULL
       OR employee_id = ''

    UNION ALL

    SELECT
        'DQ-003 Payroll records without valid employee_key' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_payroll f
    LEFT JOIN dim_employee e
        ON f.employee_key = e.employee_key
    WHERE e.employee_key IS NULL

    UNION ALL

    SELECT
        'DQ-004 Attendance records without valid employee_key' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_attendance f
    LEFT JOIN dim_employee e
        ON f.employee_key = e.employee_key
    WHERE e.employee_key IS NULL

    UNION ALL

    SELECT
        'DQ-005 Leave records without valid employee_key' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_leave f
    LEFT JOIN dim_employee e
        ON f.employee_key = e.employee_key
    WHERE e.employee_key IS NULL

    UNION ALL

    SELECT
        'DQ-006 Training records without valid employee_key' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_training f
    LEFT JOIN dim_employee e
        ON f.employee_key = e.employee_key
    WHERE e.employee_key IS NULL

    UNION ALL

    SELECT
        'DQ-007 Performance records without valid employee_key' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_performance f
    LEFT JOIN dim_employee e
        ON f.employee_key = e.employee_key
    WHERE e.employee_key IS NULL

    UNION ALL

    SELECT
        'DQ-008 Attrition records without valid employee_key' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_attrition f
    LEFT JOIN dim_employee e
        ON f.employee_key = e.employee_key
    WHERE e.employee_key IS NULL

    UNION ALL

    SELECT
        'DQ-009 Payroll annual salary less than or equal to zero' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_payroll
    WHERE annual_salary <= 0
       OR annual_salary IS NULL

    UNION ALL

    SELECT
        'DQ-010 Attendance present plus absent greater than working days' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_attendance
    WHERE present_days + absent_days > working_days

    UNION ALL

    SELECT
        'DQ-011 Performance rating outside 1 to 5' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_performance
    WHERE performance_rating < 1
       OR performance_rating > 5
       OR performance_rating IS NULL

    UNION ALL

    SELECT
        'DQ-012 Potential rating outside 1 to 5' AS check_name,
        COUNT(*) AS issue_count
    FROM fact_performance
    WHERE potential_rating < 1
       OR potential_rating > 5
       OR potential_rating IS NULL

    UNION ALL

    SELECT
        'DQ-013 Duplicate date_key in dim_date' AS check_name,
        COUNT(*) AS issue_count
    FROM (
        SELECT
            date_key
        FROM dim_date
        GROUP BY
            date_key
        HAVING COUNT(*) > 1
    )

    UNION ALL

    SELECT
        'DQ-014 Invalid RLS access type' AS check_name,
        COUNT(*) AS issue_count
    FROM dim_security_user
    WHERE access_type NOT IN ('ALL', 'DEPARTMENT', 'LOCATION', 'RESTRICTED')

    UNION ALL

    SELECT
        'DQ-015 Missing RLS user email' AS check_name,
        COUNT(*) AS issue_count
    FROM dim_security_user
    WHERE user_email IS NULL
       OR user_email = ''
       OR user_email NOT LIKE '%@%'

    UNION ALL

    SELECT
        'DQ-016 Department access value not found in dim_department' AS check_name,
        COUNT(*) AS issue_count
    FROM dim_security_user s
    LEFT JOIN dim_department d
        ON s.department = d.department_name
    WHERE s.access_type = 'DEPARTMENT'
      AND d.department_key IS NULL

    UNION ALL

    SELECT
        'DQ-017 Location access value not found in dim_location' AS check_name,
        COUNT(*) AS issue_count
    FROM dim_security_user s
    LEFT JOIN dim_location l
        ON s.location = l.location
    WHERE s.access_type = 'LOCATION'
      AND l.location_key IS NULL
);