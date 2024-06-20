import pandas as pd
import sqlite3
from datetime import datetime
import re


def load_data_to_db(csv_file):
    # Extract date from the CSV filename assuming format 'sto_YYYYMMDD.csv'
    date_match = re.search(r"sto_(\d{8})\.csv", csv_file)
    table_name = date_match.group(1) if date_match else datetime.now().strftime('%Y%m%d')

    # The database file will be named 'sto.db'
    db_file = 'sto.db'

    # Load CSV file into DataFrame, excluding the 'Description' column
    df = pd.read_csv(csv_file, usecols=lambda column: column not in ['Description'])

    # Add a timestamp column for when the data is loaded
    df['Loaded_Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    # Load data into the database, append if the table already exists
    df.to_sql(table_name, conn, if_exists='append', index=False)

    # Close the connection
    conn.close()
    print(f"Data has been successfully loaded into table {table_name} in {db_file}")


# Specify the CSV file
csv_file = 'sto_20240620.csv'

# Call the function to load data
load_data_to_db(csv_file)
