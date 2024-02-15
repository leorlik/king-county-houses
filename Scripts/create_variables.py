import sqlite3


def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('../data/kc_house_data.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Read the SQL queries from the file
    with open('sql/create_variables.sql', 'r') as file:
        sql_queries = file.read().replace("\n", "").replace("\t", " ")
        file.close()

    # Execute the SQL queries
    cursor.executescript(sql_queries)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()