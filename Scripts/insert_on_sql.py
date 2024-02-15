import pandas as pd
from datetime import datetime
import os
import sqlite3

PATH_TO_CSV = '../data/kc_house_data.csv'

def convert_dtype(value):
    # Convert datetime to string in ISO format
    if isinstance(value, pd.Timestamp):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    # Convert float to string
    elif isinstance(value, float):
        return str(value)
    # For other types, return as is
    else:
        return value


def insert_dataframe_to_sql(dataframe, table_name):
    # Connect to SQLite in-memory database
    
    conn = sqlite3.connect('../data/kc_house_data.db')

    # Read the SQL file
    f = open(os.path.join("sql","create_") + table_name + ".sql",
              "r")
    create_query = f.read()
    f.close()
    create_query = create_query.replace("\n", "").replace("\t", "")

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the create query
    cursor.execute(create_query)

    # Insert the dataframe into the table
    for index,row in dataframe.iterrows():
        row_values = [convert_dtype(value) for value in row]
        cursor.execute(f"INSERT INTO {table_name} ({','.join(dataframe.columns)}) VALUES ({','.join(['?']*len(dataframe.columns))})", tuple(row_values))


    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

def main():

    df = pd.read_csv(PATH_TO_CSV)

    date_format = "%Y%m%dT%H%M%S"

    df["date"] = df["date"].apply(lambda x: datetime.strptime(x, date_format))
    df[["id"]] = df[["id"]].astype(str)
    sales_dataset = df[['id', 'date', 'price']]
    sales_dataset.rename(columns={'date': 'sales_date'}, inplace=True)
    house_dataset = df.drop(['date', 'price'], axis=1).drop_duplicates()

    insert_dataframe_to_sql(sales_dataset, 'sales_table')
    insert_dataframe_to_sql(house_dataset, 'house_table')

if __name__ == "__main__":
    main()