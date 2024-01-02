from copy_tables import copy_table
from data_quality_monitor import get_tables_and_columns, monitor_data_quality
from dotenv import load_dotenv
import os
import schedule
import time

# Load environment variables from .env
load_dotenv()

# Get the source connection string
source_conn_str = os.getenv("SOURCE_CONN_STR")

# Get the destination connection string
dest_conn_str = os.getenv("DEST_CONN_STR")

# Get the report filename
report_filename = os.getenv("REPORT_FILENAME")

def main():
    last_update_dict = {}

    # List of tables to copy
    tables_to_copy = ['actor', 'category', 'film', 'film_actor', 'film_category', 'inventory', 'language']

    # Copy each table
    for table in tables_to_copy:
        copy_table(source_conn_str, dest_conn_str, table, last_update_dict)

    # Get tables and columns dynamically
    tables_and_columns = get_tables_and_columns()

    # Call the function to monitor data quality
    monitor_data_quality(tables_and_columns, report_filename)

# Schedule the main function to run every day at 11 pm
schedule.every().day.at("23:00").do(main)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)