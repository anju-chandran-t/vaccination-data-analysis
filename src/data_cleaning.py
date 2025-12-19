import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
CLEAN_PATH = os.path.join(BASE_DIR, "data", "cleaned")

os.makedirs(CLEAN_PATH, exist_ok=True)

def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def clean_coverage():
    df = read_csv_safe(os.path.join(RAW_PATH, "coverage-data.csv"))

    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['coverage'] = pd.to_numeric(df['coverage'], errors='coerce')
    df['target_number'] = pd.to_numeric(df['target_number'], errors='coerce')
    df['doses_administered'] = pd.to_numeric(df['doses'], errors='coerce')

    # Compute coverage if missing
    # mask = df['coverage'].isna() & df['dodge'].notna() & df['target_number'].notna()
    # df.loc[mask, 'coverage'] = (df.loc[mask, 'dodge'] / df.loc[mask, 'target_number']) * 100
    # Only calculate if target_number is greater than 0
    mask = (df['coverage'].isna() & 
        df['doses_administered'].notna() & 
        (df['target_number'] > 0))

    df.loc[mask, 'coverage'] = (df.loc[mask, 'doses_administered'] / df.loc[mask, 'target_number']) * 100

    df.dropna(subset=['code', 'year'], inplace=True)
    df.to_csv(os.path.join(CLEAN_PATH, "coverage_clean.csv"), index=False)

def clean_incidence():
    df = read_csv_safe(os.path.join(RAW_PATH, "incidence-rate-data.csv"))

    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df['incidence_rate'] = pd.to_numeric(df['incidence_rate'], errors='coerce')
    df.dropna(subset=['code', 'year'], inplace=True)
    df.to_csv(os.path.join(CLEAN_PATH, "incidence_rate_clean.csv"), index=False)

def clean_reported_cases():
    df = read_csv_safe(os.path.join(RAW_PATH, "reported-cases-data.csv"))

    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df['cases'] = pd.to_numeric(df['cases'], errors='coerce').fillna(0)
    df.to_csv(os.path.join(CLEAN_PATH, "reported_cases_clean.csv"), index=False)

def clean_vaccine_intro():
    df = read_csv_safe(os.path.join(RAW_PATH, "vaccine-introduction-data.csv"))

    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df['intro'] = df['intro'].map({'Yes': 1, 'No': 0})
    df.to_csv(os.path.join(CLEAN_PATH, "vaccine_intro_clean.csv"), index=False)

def clean_vaccine_schedule():
    df = read_csv_safe(os.path.join(RAW_PATH, "vaccine-schedule-data.csv"))

    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df.to_csv(os.path.join(CLEAN_PATH, "vaccine_schedule_clean.csv"), index=False)

if __name__ == "__main__":
    clean_coverage()
    clean_incidence()
    clean_reported_cases()
    clean_vaccine_intro()
    clean_vaccine_schedule()
