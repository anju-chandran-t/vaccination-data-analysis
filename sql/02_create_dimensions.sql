/*DROP TABLE IF EXISTS dim_country;*/

CREATE TABLE dim_country (
    country_id INT IDENTITY PRIMARY KEY,
    code NVARCHAR(100) UNIQUE,
    name NVARCHAR(255),
    group_name NVARCHAR(100)
);

INSERT INTO dim_country (code, name, group_name)
SELECT DISTINCT code, name, group_name
FROM stg_coverage;



DROP TABLE IF EXISTS dim_year;

CREATE TABLE dim_year (
    year_id INT IDENTITY PRIMARY KEY,
    year INT UNIQUE
);

INSERT INTO dim_year (year)
SELECT DISTINCT year FROM stg_coverage
WHERE year IS NOT NULL;

DROP TABLE IF EXISTS dim_antigen;

CREATE TABLE dim_antigen (
    antigen_id INT IDENTITY PRIMARY KEY,
    antigen NVARCHAR(100),
    antigen_description NVARCHAR(255)
);


INSERT INTO dim_antigen (antigen, antigen_description)
SELECT DISTINCT antigen, antigen_description
FROM stg_coverage;


DROP TABLE IF EXISTS dim_disease;

CREATE TABLE dim_disease (
    disease_id INT IDENTITY PRIMARY KEY,
    disease NVARCHAR(100),
    disease_description NVARCHAR(255)
);

INSERT INTO dim_disease (disease, disease_description)
SELECT DISTINCT disease, disease_description
FROM stg_incidence_rate;
