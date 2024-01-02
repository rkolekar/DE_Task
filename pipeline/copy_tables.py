import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime


def copy_table(source_conn_str, dest_conn_str, table_name, last_update_dict):
    # Source connection
    source_engine = create_engine(source_conn_str)

    # Destination connection
    dest_engine = create_engine(dest_conn_str)

    # Query to fetch data based on last update timestamp
    last_update = last_update_dict.get(table_name, datetime(1970, 1, 1))

    # Construct the query based on the available columns
    columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
    columns_df = pd.read_sql_query(columns_query, source_engine)
    columns_list = columns_df['column_name'].tolist()

    # Check if 'last_update' is present in the columns
    if 'last_update' in columns_list:
        query = f"SELECT * FROM {table_name} WHERE last_update > '{last_update}'"
    else:
        query = f"SELECT * FROM {table_name}"

    # Fetch data from source
    df = pd.read_sql_query(query, source_engine)

    if not df.empty:
        # Copy data to destination
        df.to_sql(table_name, dest_engine, index=False,
                  if_exists='append')  # Use 'replace' or 'append' based on your needs
        print(f"Table '{table_name}' copied.")
    else:
        print(f"Table '{table_name}' has no updates since '{last_update}'. Skipping.")

    # Update last update timestamp in the dictionary
    last_update_dict[table_name] = datetime.now()