USE VaccinationDB;
GO

CREATE TABLE stg_coverage (
    group_name NVARCHAR(100),
    code NVARCHAR(100),
    name NVARCHAR(255),
    year INT,
    antigen NVARCHAR(100),
    antigen_description NVARCHAR(255),
    coverage_category NVARCHAR(100),
    coverage_category_description NVARCHAR(255),
    target_number BIGINT,
    doses_administered BIGINT,
    coverage FLOAT
);

CREATE TABLE stg_incidence_rate (
    group_name NVARCHAR(100),
    code NVARCHAR(100),
    name NVARCHAR(255),
    year INT,
    disease NVARCHAR(100),
    disease_description NVARCHAR(255),
    denominator NVARCHAR(100),
    incidence_rate FLOAT
);

CREATE TABLE stg_reported_cases (
    group_name NVARCHAR(100),
    code NVARCHAR(100),
    name NVARCHAR(255),
    year INT,
    disease NVARCHAR(100),
    disease_description NVARCHAR(255),
    cases BIGINT
);
