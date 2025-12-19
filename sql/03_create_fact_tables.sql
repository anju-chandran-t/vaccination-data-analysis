DROP TABLE IF EXISTS fact_coverage;

CREATE TABLE fact_coverage (
    coverage_id INT IDENTITY PRIMARY KEY,
    country_id INT,
    year_id INT,
    antigen_id INT,
    target_number BIGINT,
    doses_administered BIGINT,
    coverage FLOAT,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (year_id) REFERENCES dim_year(year_id),
    FOREIGN KEY (antigen_id) REFERENCES dim_antigen(antigen_id)
);

INSERT INTO fact_coverage (
    country_id, year_id, antigen_id,
    target_number, doses_administered, coverage
)
SELECT
    c.country_id,
    y.year_id,
    a.antigen_id,
    s.target_number,
    s.doses_administered,
    s.coverage
FROM stg_coverage s
JOIN dim_country c ON s.code = c.code
JOIN dim_year y ON s.year = y.year
JOIN dim_antigen a ON s.antigen = a.antigen;

DROP TABLE IF EXISTS fact_incidence_rate;

CREATE TABLE fact_incidence_rate (
    incidence_id INT IDENTITY PRIMARY KEY,
    country_id INT,
    year_id INT,
    disease_id INT,
    incidence_rate FLOAT,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (year_id) REFERENCES dim_year(year_id),
    FOREIGN KEY (disease_id) REFERENCES dim_disease(disease_id)
);


INSERT INTO fact_incidence_rate (
    country_id, year_id, disease_id, incidence_rate
)
SELECT
    c.country_id,
    y.year_id,
    d.disease_id,
    s.incidence_rate
FROM stg_incidence_rate s
JOIN dim_country c ON s.code = c.code
JOIN dim_year y ON s.year = y.year
JOIN dim_disease d ON s.disease = d.disease;

DROP TABLE IF EXISTS fact_reported_cases;

CREATE TABLE fact_reported_cases (
    case_id INT IDENTITY PRIMARY KEY,
    country_id INT,
    year_id INT,
    disease_id INT,
    cases INT,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (year_id) REFERENCES dim_year(year_id),
    FOREIGN KEY (disease_id) REFERENCES dim_disease(disease_id)
);

INSERT INTO fact_reported_cases (
    country_id, year_id, disease_id, cases
)
SELECT
    c.country_id,
    y.year_id,
    d.disease_id,
    s.cases
FROM stg_reported_cases s
JOIN dim_country c ON s.code = c.code
JOIN dim_year y ON s.year = y.year
JOIN dim_disease d ON s.disease = d.disease;


SELECT COUNT(*) FROM fact_coverage;
SELECT COUNT(*) FROM fact_incidence_rate;
SELECT COUNT(*) FROM fact_reported_cases;
