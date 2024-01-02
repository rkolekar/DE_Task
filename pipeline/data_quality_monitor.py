from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from tabulate import tabulate
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the source connection string
source_conn_str = os.getenv("SOURCE_CONN_STR")

# Establish connection
source_engine = create_engine(source_conn_str)


def get_tables_and_columns():
    # Query to get tables and columns from information schema
    query = """
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_name NOT IN ('database_firewall_rules', 'sysdiagrams')
    """

    # Execute the query and load data into a DataFrame
    tables_and_columns_df = pd.read_sql_query(query, source_engine)

    # Group by table name to get a dictionary of tables and their columns
    tables_and_columns = tables_and_columns_df.groupby('table_name')['column_name'].unique().to_dict()

    return tables_and_columns


def monitor_data_quality(tables_and_columns, report_filename):
    reports = []

    for table, columns in tables_and_columns.items():
        characteristics_query = f"SELECT COUNT(*) AS total_records, COUNT(DISTINCT {columns[0]}) AS distinct_records FROM {table}"
        characteristics_report = pd.read_sql_query(characteristics_query, source_engine)

        report = f"\n<h2 style='font-weight: bold;'>Monitoring Data Quality for Table: {table}</h2>\n"
        report += "<h3>Characteristics Report:</h3>"
        report += tabulate(characteristics_report, headers='keys', tablefmt='html') + "\n"

        for column in columns:
            uniqueness_query = f"SELECT {column}, COUNT(*) AS occurrence FROM {table} GROUP BY {column} HAVING COUNT(*) > 1"
            uniqueness_report = pd.read_sql_query(uniqueness_query, source_engine)
            report += f"\n<h3>Uniqueness Report for Column: {column}</h3>"
            report += tabulate(uniqueness_report, headers='keys', tablefmt='html') + "\n"

            integrity_query = f"SELECT COUNT(*) AS null_count FROM {table} WHERE {column} IS NULL"
            integrity_report = pd.read_sql_query(integrity_query, source_engine)
            report += f"\n<h3>Integrity Report for Column: {column}</h3>"
            report += tabulate(integrity_report, headers='keys', tablefmt='html') + "\n"

        reports.append(report)

    # Generate the filename with the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{report_filename}{current_date}.html"

    # Save reports to the HTML file
    with open(filename, "w") as file:
        file.write("<html><head><style>body { font-family: Arial, sans-serif; }</style></head><body>")
        file.write("<h1>Data Quality Monitoring Report</h1>")
        for report in reports:
            file.write(report)
        file.write("</body></html>")
        print(f"Report is saved at {filename}")