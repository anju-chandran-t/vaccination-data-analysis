import os
import numpy as np
import pandas as pd
import urllib
from sqlalchemy import create_engine

# ==================================================
# PROJECT PATHS
# ==================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_PATH = os.path.join(BASE_DIR, "data", "cleaned")

# ==================================================
# SQL SERVER CONNECTION (WINDOWS AUTH)
# ==================================================
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"   # change if your instance name differs
    "DATABASE=VaccinationDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# ==================================================
# HELPER FUNCTION
# ==================================================
def load_csv(filename):
    path = os.path.join(CLEAN_PATH, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")
    return pd.read_csv(path, encoding="latin1")


==================================================
LOAD COVERAGE DATA → stg_coverage
==================================================
df_cov = load_csv("coverage_clean.csv")

# Standardize column names
df_cov.columns = (
    df_cov.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Align dataframe schema with SQL table
df_cov = df_cov.rename(columns={
    "group": "group_name",
    "doses": "doses_administered",
    "dodge": "doses_administered"
})

coverage_cols = [
    "group_name",
    "code",
    "name",
    "year",
    "antigen",
    "antigen_description",
    "coverage_category",
    "coverage_category_description",
    "target_number",
    "doses_administered",
    "coverage"
]

df_cov = df_cov[[c for c in coverage_cols if c in df_cov.columns]]
df_cov = df_cov.loc[:, ~df_cov.columns.duplicated()]

# -----------------------------
# FIX NUMERIC DATA ISSUES
# -----------------------------
# 1. Handle Infinity values (the cause of your previous crash)
df_cov = df_cov.replace([np.inf, -np.inf], np.nan)

# 2. Year is safe as a standard Int64
df_cov['year'] = pd.to_numeric(df_cov['year'], errors='coerce').round(0).astype('Int64')

# 3. Use 'Float64' for large numbers to prevent SQL overflow during the 'to_sql' handshake,
# or ensure they are treated as large integers.
for col in ["target_number", "doses_administered"]:
    if col in df_cov.columns:
        # We convert to float first to handle NaNs, then round
        df_cov[col] = pd.to_numeric(df_cov[col], errors='coerce').round(0).astype('Int64')

# 4. Coverage rounding
df_cov['coverage'] = pd.to_numeric(df_cov['coverage'], errors='coerce').round(0).astype('Int64')

# 5. CRITICAL: Replace NaN with None so SQLAlchemy sends NULL to SQL Server
df_cov = df_cov.replace({np.nan: None})

# print(df_cov.head())
# type_counts = df_cov['year'].apply(type).value_counts()
# print("Data types in 'year' column:\n", type_counts)

df_cov.to_sql(
    "stg_coverage",
    engine,
    if_exists="append",
    index=False,
    chunksize=500          # SQL Server safe
)

print("✅ Loaded coverage_clean.csv into stg_coverage")


# ==================================================
# LOAD INCIDENCE RATE DATA → stg_incidence_rate
# ==================================================
df_inc = load_csv("incidence_rate_clean.csv")

# 1. Standardize and Rename
df_inc.columns = df_inc.columns.str.strip().str.lower().str.replace(" ", "_")
df_inc = df_inc.rename(columns={"group": "group_name"})

# 2. Fix Numeric Issues
import numpy as np

# Convert Year to Nullable Integer (2023.0 -> 2023)
df_inc["year"] = pd.to_numeric(df_inc["year"], errors="coerce").round(0).astype("Int64")

# # Ensure Incidence Rate is Float and handle Infinity/NaN
# df_inc["incidence_rate"] = pd.to_numeric(df_inc["incidence_rate"], errors="coerce")
# df_inc = df_inc.replace([np.inf, -np.inf], np.nan)

# Replace NaN with None (Essential for pyodbc to send NULL to SQL)
df_inc = df_inc.replace({np.nan: None})

# 3. Select final columns
incidence_cols = [
    "group_name", "code", "name", "year", 
    "disease", "disease_description", "denominator", "incidence_rate"
]
df_inc = df_inc[[c for c in incidence_cols if c in df_inc.columns]]

# 4. Load to SQL
df_inc.to_sql(
    "stg_incidence_rate",
    engine,
    if_exists="append", # Use "replace" once if you need to fix column sizes
    index=False,
    chunksize=1000
)

print("✅ Loaded incidence_rate_clean.csv into stg_incidence_rate")

# ==================================================
# LOAD REPORTED CASES DATA → stg_reported_cases
# ==================================================
df_cases = load_csv("reported_cases_clean.csv")

# 1. Standardize and Rename
df_cases.columns = df_cases.columns.str.strip().str.lower().str.replace(" ", "_")
df_cases = df_cases.rename(columns={"group": "group_name"})

# 2. Fix Numeric Issues
import numpy as np

# Convert Year to Nullable Integer (2023.0 -> 2023)
df_cases["year"] = pd.to_numeric(df_cases["year"], errors="coerce").round(0).astype("Int64")

# Convert Cases to Big Integer (1.0 -> 1)
# We round first in case there are decimals, then cast to Int64 for SQL compatibility
df_cases["cases"] = pd.to_numeric(df_cases["cases"], errors="coerce").round(0).astype("Int64")

# 3. Final Cleanup: Replace NaN with None (Essential for SQL NULL)
df_cases = df_cases.replace({np.nan: None})

# 4. Select final columns
cases_cols = [
    "group_name", "code", "name", "year", 
    "disease", "disease_description", "cases"
]
df_cases = df_cases[[c for c in cases_cols if c in df_cases.columns]]

# 5. Load to SQL
df_cases.to_sql(
    "stg_reported_cases",
    engine,
    if_exists="append", # Use "replace" once if you need to fix existing column types
    index=False,
    chunksize=1000
)

print("✅ Loaded reported_cases_clean.csv into stg_reported_cases")

# # ==================================================
# print("🎉 ALL STAGING TABLES LOADED SUCCESSFULLY")
