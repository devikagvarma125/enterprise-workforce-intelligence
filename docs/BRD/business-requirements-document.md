# Business Requirements Document  
## Enterprise Workforce Intelligence Platform

---

## 1. Project Overview

The Enterprise Workforce Intelligence Platform is an end-to-end HR analytics and workforce intelligence project designed to simulate how an organisation can use modern cloud-based data architecture to understand its workforce.

The project uses a realistic business scenario where HR data is generated from multiple source areas such as employee records, payroll, attendance, leave, recruitment, training, performance, and attrition. The data is stored in Azure Data Lake Storage Gen2, transformed using Azure Databricks, modelled into a Lakehouse structure, and visualised using Power BI.

The final solution will include:

- Synthetic HR source datasets
- Azure Data Lakehouse architecture
- Raw, Bronze, Silver, and Gold data layers
- Databricks notebooks for data transformation
- Delta-style analytical tables
- SQL analysis queries
- Power BI Desktop report
- Power BI Service publishing
- Row-Level Security for business users
- Basic employee attrition prediction model
- Professional GitHub documentation

This is a self-developed portfolio project based on a realistic enterprise analytics scenario. It is designed to demonstrate practical skills in business analysis, data engineering, SQL, Power BI, cloud analytics, dashboard design, and machine learning.

---

## 2. Business Scenario

ABC Global Services Ltd is a fictional medium-to-large organisation with employees across multiple departments, locations, job roles, and work modes.

The HR leadership team currently receives workforce data from different systems and spreadsheets. These include employee master records, payroll files, attendance logs, recruitment trackers, training records, performance review files, and employee exit records.

Because the data is spread across multiple systems, the organisation does not have a single trusted view of its workforce. Reports are prepared manually, which can be time-consuming, inconsistent, and difficult to validate.

The organisation wants to build a cloud-based workforce intelligence platform that allows HR and senior leadership to monitor workforce performance, attrition, salary cost, recruitment, attendance, training, and employee performance from one central reporting model.

The solution should also support secure report access, so managers and business users only see the workforce data they are authorised to view.

---

## 3. Business Problem

The main business problem is the lack of a centralised, reliable, and secure HR analytics platform.

Current challenges include:

- HR data is stored across disconnected files and systems.
- Manual reporting takes time and increases the risk of errors.
- Leadership cannot easily track workforce trends across departments and locations.
- Attrition is difficult to analyse by department, job role, location, tenure, salary band, and performance.
- Recruitment performance is not monitored consistently.
- Attendance, leave, training, performance, payroll, and attrition data are not connected.
- HR teams have limited ability to identify possible attrition risk factors.
- Business users depend on static reports rather than interactive dashboards.
- Report access is not personalised based on user role or department responsibility.
- There is no structured cloud-based data pipeline for repeatable reporting.

---

## 4. Project Objectives

The objectives of this project are to:

1. Create realistic synthetic HR datasets for a fictional organisation.
2. Store source data in an Azure Data Lakehouse-style structure.
3. Build Raw, Bronze, Silver, and Gold data layers.
4. Use Azure Databricks notebooks to clean, transform, and model HR data.
5. Create reporting-ready Gold tables for Power BI.
6. Design a dimensional data model suitable for workforce analytics.
7. Write SQL queries for business analysis and data validation.
8. Build a Power BI report covering key HR analytics areas.
9. Publish the report to Power BI Service.
10. Implement Row-Level Security so users only see authorised data.
11. Build a basic employee attrition prediction model.
12. Document the project clearly for GitHub, CV, LinkedIn, and interview discussions.

---

## 5. Project Scope

### 5.1 In Scope

The project will cover:

- Synthetic HR data generation
- Azure Data Lake Storage Gen2 structure
- Raw data layer
- Bronze data layer
- Silver data layer
- Gold data layer
- Azure Databricks notebooks
- Delta-style Lakehouse table design
- Employee master data
- Department and job role analysis
- Location and work mode analysis
- Payroll and salary analysis
- Attendance and absence analysis
- Leave analysis
- Recruitment analysis
- Training analysis
- Performance analysis
- Attrition analysis
- Employee attrition prediction
- SQL analysis queries
- Data quality checks
- Power BI Desktop report development
- Power BI Service publishing
- Row-Level Security design and implementation
- Documentation and interview explanation

### 5.2 Out of Scope

The following items are not included in the first version:

- Real employee data
- Real HR system API integration
- Real-time data streaming
- Production deployment of machine learning model
- Complex MLOps pipeline
- Enterprise-grade CI/CD deployment
- Advanced HR recommendation engine
- Automated enterprise identity governance
- Production-level security audit

These can be considered as future enhancements.

---

## 6. Target Users and Stakeholders

| Stakeholder | Purpose |
|---|---|
| HR Director | Needs high-level workforce trends, attrition, headcount, salary, and diversity insights |
| HR Business Partner | Needs department-level HR metrics and employee trends |
| Recruitment Manager | Needs hiring, source, and time-to-hire insights |
| Department Manager | Needs team-level headcount, absence, performance, and attrition insights |
| Finance Team | Needs salary cost and workforce cost analysis |
| Executive Leadership | Needs strategic workforce KPIs and trends |
| Data Analyst / BI Developer | Builds, validates, documents, and maintains the analytics solution |
| Power BI Report Viewer | Consumes secured reports in Power BI Service |
| Azure / Data Platform User | Manages data storage, transformation, and data pipeline execution |

---

## 7. Business Questions

The solution should answer the following business questions.

### 7.1 Workforce Overview

- What is the current total headcount?
- How is headcount distributed by department, location, job role, gender, and work mode?
- How has headcount changed over time?
- Which departments are growing or shrinking?
- What is the average employee tenure?
- How many employees are active, inactive, or have left?

### 7.2 Attrition Analysis

- What is the overall attrition rate?
- Which departments have the highest attrition?
- Which job roles have the highest attrition?
- Is attrition higher among certain age groups, tenure bands, or salary bands?
- Are employees with lower performance ratings more likely to leave?
- Is high absence linked to higher attrition?
- Is low training participation linked to higher attrition?
- What are the most common reasons for employees leaving?

### 7.3 Recruitment Analysis

- How many candidates were hired in each period?
- What is the average time to hire?
- Which recruitment sources produce the most hires?
- What is the offer acceptance rate?
- Which departments have the highest recruitment demand?
- How does recruitment performance vary by location?

### 7.4 Attendance and Leave Analysis

- What is the average absence rate?
- Which departments have the highest absence levels?
- How many leave days are taken by employees?
- Are there seasonal absence patterns?
- Which employees or teams show repeated absence trends?
- Are employees with high absence more likely to leave?

### 7.5 Payroll Analysis

- What is the total salary cost?
- What is the average salary by department, role, and location?
- How is salary distributed across the organisation?
- Which departments have the highest workforce cost?
- How does salary vary by job level or pay grade?
- Are there differences in average salary across locations or gender groups?

### 7.6 Training and Performance Analysis

- What percentage of employees completed training?
- Which departments have the highest training participation?
- How do performance ratings vary by department and job role?
- Is training participation linked to better performance?
- Is poor performance linked to attrition?
- Which teams may need additional training support?

### 7.7 Security and Access

- Can department managers see only their department data?
- Can location managers see only their location data?
- Can senior HR users see all workforce data?
- Can report access be personalised using the logged-in Power BI user email?
- Can RLS be tested before sharing the report?

### 7.8 Predictive Analytics

- Can historical HR data be used to estimate attrition risk?
- Which factors are most associated with employee attrition?
- How can HR use attrition risk insights for retention planning?
- How can model output be explained in a business-friendly way?

---

## 8. Key Performance Indicators

| KPI | Description |
|---|---|
| Total Headcount | Number of active employees |
| New Hires | Number of employees hired during a selected period |
| Leavers | Number of employees who left during a selected period |
| Attrition Rate | Percentage of employees who left the organisation |
| Average Tenure | Average length of service of employees |
| Total Salary Cost | Total salary cost across employees |
| Average Salary | Average employee salary |
| Absence Rate | Percentage of working days lost due to absence |
| Leave Days Taken | Total leave days used by employees |
| Training Completion Rate | Percentage of completed training records |
| Average Performance Rating | Average employee performance score |
| Time to Hire | Average number of days between application and hiring |
| Offer Acceptance Rate | Percentage of accepted job offers |
| Attrition Risk Score | Model-generated indication of employee attrition risk |

---

## 9. Data Sources

The project will use synthetic data representing the following source areas.

| Data Source | Description |
|---|---|
| Employee Data | Employee profile, department, role, manager, hire date, location, status |
| Payroll Data | Salary, bonus, salary band, pay grade |
| Attendance Data | Work days, present days, absent days, late arrivals |
| Leave Data | Annual leave, sick leave, unpaid leave |
| Recruitment Data | Candidate source, application date, offer date, hire date, hiring status |
| Training Data | Training course, completion status, training hours |
| Performance Data | Review period, performance rating, promotion flag |
| Attrition Data | Exit date, exit reason, voluntary or involuntary leaving status |
| Security Mapping Data | User email, department access, location access, role type |

---

## 10. Proposed Azure Lakehouse Architecture

The solution will follow a Lakehouse-style architecture.

```text
Synthetic HR Source Files
        ↓
Azure Data Lake Storage Gen2
        ↓
Raw Layer
        ↓
Azure Databricks
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
Databricks SQL / Gold Tables
        ↓
Power BI Desktop
        ↓
Power BI Service
        ↓
Published Report with Row-Level Security
### 10.1 Raw Layer

The Raw layer stores the original source files exactly as received or generated.  
This layer acts as the landing area for source data before any cleaning or transformation is applied.

Example Raw layer files:

```text
data/raw/employees.csv
data/raw/payroll.csv
data/raw/attendance.csv
data/raw/leave.csv
data/raw/recruitment.csv
data/raw/training.csv
data/raw/performance.csv
data/raw/attrition.csv
data/raw/security_mapping.csv
```

Key characteristics of the Raw layer:

- Stores original source data.
- No business transformations are applied.
- Maintains source-level structure.
- Used as the starting point for the data pipeline.
- Helps with traceability and reprocessing if needed.

---

### 10.2 Bronze Layer

The Bronze layer stores standardised ingested data from the Raw layer.

Typical activities in the Bronze layer include:

- Loading raw CSV files.
- Standardising column names.
- Converting file formats where required.
- Adding ingestion timestamp.
- Adding source file name.
- Preserving record-level detail.
- Performing basic schema checks.

Example Bronze layer outputs:

```text
data/bronze/bronze_employees
data/bronze/bronze_payroll
data/bronze/bronze_attendance
data/bronze/bronze_leave
data/bronze/bronze_recruitment
data/bronze/bronze_training
data/bronze/bronze_performance
data/bronze/bronze_attrition
data/bronze/bronze_security_mapping
```

The Bronze layer does not apply major business rules.  
Its purpose is to create a consistent and traceable copy of source data.

---

### 10.3 Silver Layer

The Silver layer stores cleaned, validated, and business-ready data.

Typical activities in the Silver layer include:

- Handling missing values.
- Removing duplicate records.
- Fixing invalid dates.
- Standardising department, location, and job role values.
- Validating employee IDs.
- Validating date relationships.
- Joining reference data.
- Creating clean business fields.
- Preparing data for dimensional modelling.

Example Silver layer outputs:

```text
data/silver/silver_employees
data/silver/silver_payroll
data/silver/silver_attendance
data/silver/silver_leave
data/silver/silver_recruitment
data/silver/silver_training
data/silver/silver_performance
data/silver/silver_attrition
data/silver/silver_security_mapping
```

The Silver layer is where most data quality and business validation rules are applied.

---

### 10.4 Gold Layer

The Gold layer stores reporting-ready and analytics-ready tables.

This layer is designed for Power BI reporting, SQL analysis, and machine learning use cases.

Typical Gold layer outputs include:

- Dimension tables.
- Fact tables.
- Aggregated reporting views.
- Power BI-ready datasets.
- Security mapping table for Row-Level Security.
- Attrition modelling dataset.

Example Gold layer outputs:

```text
data/gold/dim_employee
data/gold/dim_department
data/gold/dim_job_role
data/gold/dim_location
data/gold/dim_date
data/gold/dim_manager
data/gold/dim_security_user
data/gold/fact_payroll
data/gold/fact_attendance
data/gold/fact_leave
data/gold/fact_recruitment
data/gold/fact_training
data/gold/fact_performance
data/gold/fact_attrition
data/gold/ml_attrition_dataset
```

The Gold layer is the main source for the Power BI report.

---

## 11. Proposed Data Model

The Gold layer will follow a dimensional model suitable for Power BI reporting.

The model will include dimension tables and fact tables.

Dimension tables describe business entities such as employees, departments, locations, roles, managers, dates, and security users.

Fact tables store measurable business events such as payroll, attendance, leave, recruitment, training, performance, and attrition.

---

### 11.1 Dimension Tables

| Table | Purpose |
|---|---|
| DimEmployee | Stores employee profile, employment status, hire date, department, role, location, and manager details |
| DimDepartment | Stores department information |
| DimJobRole | Stores job role, job family, and job level information |
| DimLocation | Stores office location, region, and country information |
| DimDate | Stores calendar fields for time-based reporting |
| DimManager | Stores manager details and reporting structure |
| DimSecurityUser | Stores Power BI Row-Level Security user mapping |

---

### 11.2 Fact Tables

| Table | Purpose |
|---|---|
| FactPayroll | Stores salary, bonus, salary band, and pay grade information |
| FactAttendance | Stores work days, present days, absent days, and late arrivals |
| FactLeave | Stores leave type, leave start date, leave end date, and leave days |
| FactRecruitment | Stores applications, offers, hires, recruitment source, and time to hire |
| FactTraining | Stores training participation, completion status, and training hours |
| FactPerformance | Stores performance review rating, review period, and promotion flag |
| FactAttrition | Stores employee exit, exit reason, and voluntary or involuntary leaver status |

---

### 11.3 Reporting Model Purpose

The dimensional model will support:

- Workforce trend analysis.
- Department-level comparison.
- Location-level reporting.
- Role-based employee analysis.
- Salary and payroll analysis.
- Attendance and leave analysis.
- Recruitment analysis.
- Training and performance analysis.
- Attrition analysis.
- Row-Level Security in Power BI.

---

## 12. Functional Requirements

| ID | Requirement |
|---|---|
| FR-001 | The project must generate realistic synthetic HR datasets. |
| FR-002 | The project must store source files in Azure Data Lake Storage Gen2. |
| FR-003 | The project must organise data into Raw, Bronze, Silver, and Gold layers. |
| FR-004 | The project must use Azure Databricks notebooks for transformation. |
| FR-005 | The project must create cleaned Silver layer datasets. |
| FR-006 | The project must create Gold layer reporting tables. |
| FR-007 | The project must include employee, department, role, location, manager, date, and security dimensions. |
| FR-008 | The project must include fact tables for payroll, attendance, leave, recruitment, training, performance, and attrition. |
| FR-009 | The project must provide Power BI-ready datasets. |
| FR-010 | The project must include SQL queries for business analysis. |
| FR-011 | The project must include data quality checks. |
| FR-012 | The project must include DAX measures for workforce KPIs. |
| FR-013 | The project must include a Power BI Desktop report. |
| FR-014 | The project must publish the report to Power BI Service. |
| FR-015 | The project must implement Row-Level Security in Power BI. |
| FR-016 | The project must include a basic attrition prediction model. |
| FR-017 | The project must include clear documentation for GitHub and interview explanation. |

---

## 13. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-001 | The project must not use real personal employee data. |
| NFR-002 | The repository must be organised and easy to understand. |
| NFR-003 | Code and notebooks should be readable and reusable. |
| NFR-004 | The data pipeline should be repeatable from raw data to final output. |
| NFR-005 | The dashboard should be clear and business-friendly. |
| NFR-006 | Documentation should be suitable for GitHub and recruiter review. |
| NFR-007 | The machine learning output should be presented as a portfolio demonstration, not a real HR decision-making tool. |
| NFR-008 | Azure resources should be configured with cost control in mind. |
| NFR-009 | Databricks compute should not be left running unnecessarily. |
| NFR-010 | Row-Level Security should be tested before the report is shared with users. |
| NFR-011 | Credentials, access keys, connection strings, and tokens must not be committed to GitHub. |

---

## 14. Power BI Requirements

The Power BI report will include multiple pages designed for different HR and management use cases.

| Dashboard Page | Purpose |
|---|---|
| Executive Overview | High-level workforce KPIs for senior leadership |
| Workforce Demographics | Headcount by department, location, gender, role, and work mode |
| Attrition Analysis | Attrition trends, leaver profile, and possible attrition drivers |
| Recruitment Analysis | Hiring trends, time to hire, and recruitment source effectiveness |
| Attendance and Leave | Absence trends, leave usage, and department comparisons |
| Payroll Analysis | Salary cost, average salary, and salary distribution |
| Training and Performance | Training completion, performance ratings, and development insights |
| Attrition Prediction | Model output, attrition risk groups, and key contributing factors |

---

### 14.1 Planned Power BI Features

The Power BI report should include:

- KPI cards.
- Trend charts.
- Bar charts.
- Matrix visuals.
- Department and location slicers.
- Date filters.
- Drill-through pages where useful.
- Tooltip pages where useful.
- Clear page navigation.
- Business-friendly formatting.
- Consistent theme and layout.

---

## 15. Power BI Service and Row-Level Security Requirements

The project will include publishing the Power BI report to Power BI Service.

Planned Power BI Service tasks include:

- Publish the Power BI report from Power BI Desktop.
- Create or use a Power BI workspace for the project.
- Configure semantic model settings.
- Configure credentials or connection settings.
- Assign users to Row-Level Security roles.
- Test the report using different user access scenarios.
- Capture screenshots for documentation.

---

### 15.1 Row-Level Security Design

The project will implement dynamic Row-Level Security using a security mapping table.

The security mapping table will define what each user is allowed to see.

Example security mapping:

| User Email | Access Type | Department | Location |
|---|---|---|---|
| hr.director@abcglobal.com | ALL | ALL | ALL |
| manager.sales@abcglobal.com | DEPARTMENT | Sales | ALL |
| manager.finance@abcglobal.com | DEPARTMENT | Finance | ALL |
| manager.london@abcglobal.com | LOCATION | ALL | London |
| manager.manchester@abcglobal.com | LOCATION | ALL | Manchester |

---

### 15.2 RLS Access Scenarios

The RLS design should support the following access scenarios:

| User Type | Access Level |
|---|---|
| HR Director | Can view all departments and all locations |
| HR Business Partner | Can view assigned departments or locations |
| Department Manager | Can view only their department |
| Location Manager | Can view only their location |
| Restricted Viewer | Can view only specifically assigned data |

---

### 15.3 RLS Testing Requirements

RLS should be tested before the report is shared.

Testing should confirm that:

- HR users can view all workforce data.
- Department managers can view only their department data.
- Location managers can view only their location data.
- Restricted users cannot view unauthorised departments or locations.
- The logged-in Power BI user email correctly controls data visibility.
- RLS filters apply correctly across all report pages.

---

## 16. Azure Implementation Requirements

The Azure implementation should include the following components.

| Area | Requirement |
|---|---|
| Storage Account | Create or use an Azure Storage Account with Data Lake Gen2 capability |
| Containers / Folders | Create folders for Raw, Bronze, Silver, and Gold layers |
| Databricks Workspace | Use Azure Databricks for notebook-based transformation |
| Databricks Compute | Use small development compute suitable for portfolio work |
| Data Format | Store processed data in structured Lakehouse tables |
| Gold Layer | Make Gold tables available for reporting |
| SQL Access | Use Databricks SQL or Gold views for analytical queries |
| Power BI Connection | Connect Power BI to the Gold reporting layer |
| Cost Control | Use minimal compute and shut down resources when not needed |

---

### 16.1 Azure Cost Control Requirements

To avoid unnecessary Azure costs, the project should follow these practices:

- Use a small dataset.
- Use small development compute.
- Enable Databricks auto-termination.
- Stop Databricks clusters when not in use.
- Avoid leaving SQL warehouses running unnecessarily.
- Delete unused resources after testing if needed.
- Set Azure budget alerts where possible.
- Avoid committing keys, secrets, or connection strings to GitHub.

---

## 17. Data Security Requirements

The project will include the following data security considerations:

- No real personal employee data will be used.
- All employee records will be synthetically generated.
- Power BI Row-Level Security will restrict report data based on user access.
- A security mapping table will define authorised access.
- RLS will be documented and tested.
- Sensitive credentials will not be committed to GitHub.
- Azure keys, connection strings, and tokens must not be stored in the repository.
- Sample email addresses used for RLS will be fictional.

---

## 18. Testing Requirements

Testing will cover both data pipeline validation and report-level validation.

| Test Area | Example Checks |
|---|---|
| Raw Data Validation | Source files exist and contain expected columns |
| Bronze Validation | Files are ingested and standardised successfully |
| Silver Validation | Duplicates, missing values, and invalid dates are handled |
| Gold Validation | Dimension and fact tables are created correctly |
| Relationship Validation | Keys between dimension and fact tables match correctly |
| KPI Validation | Power BI measures return expected results |
| RLS Validation | Users see only authorised data |
| ML Validation | Attrition model produces interpretable output |

---

### 18.1 Data Quality Checks

The project should include checks for:

- Missing employee IDs.
- Duplicate employee IDs.
- Invalid hire dates.
- Exit dates before hire dates.
- Invalid department values.
- Invalid location values.
- Missing salary values.
- Negative salary values.
- Missing performance ratings.
- Invalid attendance values.
- Fact records without matching employee records.

---

## 19. Assumptions

The project is based on the following assumptions:

- All data used in the project is synthetic.
- The fictional organisation has multiple departments, job roles, and locations.
- Historical employee lifecycle data is available.
- Azure resources will be used for portfolio demonstration purposes.
- Power BI will use Gold layer tables as the reporting dataset.
- The first version may be built locally first and then implemented in Azure.
- The architecture is inspired by enterprise Lakehouse patterns.
- Row-Level Security will be tested using sample user emails.
- The Power BI Service publishing step depends on available Power BI licensing and workspace permissions.

---

## 20. Risks and Limitations

| Risk / Limitation | Mitigation |
|---|---|
| Synthetic data may not fully represent real HR data | Use realistic fields, values, and relationships |
| Azure services may create cost | Use small resources, budget alerts, and shut down compute |
| Databricks compute may be left running | Enable auto-termination and manually stop compute |
| Power BI Service features may depend on licence | Document licence assumptions and use available features |
| RLS may be configured incorrectly | Test using multiple sample users |
| Attrition model may not be highly accurate | Focus on explainability and business interpretation |
| Dashboard may become too crowded | Use separate dashboard pages for each business area |
| Project may become too large | Build in milestones |
| Power BI file cannot be previewed easily in GitHub | Add screenshots and DAX documentation |

---

## 21. Success Criteria

The project will be considered successful when:

- The repository contains clear business and technical documentation.
- Synthetic HR data is generated successfully.
- Source data is stored in a Raw layer.
- Bronze, Silver, and Gold data layers are created.
- Databricks notebooks transform the data successfully.
- Gold tables are ready for Power BI reporting.
- SQL queries produce useful workforce insights.
- Power BI dashboards answer the main business questions.
- The report is published to Power BI Service.
- Row-Level Security is implemented and tested.
- An attrition prediction model is created and explained.
- The final GitHub repository looks professional.
- The project can be confidently explained in interviews.

---

## 22. Future Enhancements

Possible future enhancements include:

- Azure Data Factory orchestration.
- Scheduled pipeline refresh.
- Power BI scheduled refresh.
- Power BI deployment pipelines.
- Incremental refresh.
- Row-level and object-level security.
- Microsoft Entra group-based access.
- Advanced forecasting.
- Employee engagement sentiment analysis.
- Advanced machine learning models.
- HR recommendation engine for retention planning.
- CI/CD for notebooks and Power BI assets.