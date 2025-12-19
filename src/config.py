SQL_SERVER = "localhost"
DATABASE = "VaccinationDB"
USERNAME = "sa"
PASSWORD = "YourPassword"

CONN_STR = (
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SQL_SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
