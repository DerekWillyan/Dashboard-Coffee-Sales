import pandas as pd
import mysql.connector
from mysql.connector import Error

def csv_to_sql(csv_file_path, table_name, host, database, user, password):
    # Load CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Create SQL statements for creating the table and inserting the data
    create_table_query = f"CREATE TABLE {table_name} ("
    for column in df.columns:
        create_table_query += f"{column} VARCHAR(255),"
    create_table_query = create_table_query.rstrip(',') + ');'
    
    insert_into_query = f"INSERT INTO {table_name} ("
    insert_into_query += ', '.join(df.columns) + ') VALUES '
    
    values = []
    for _, row in df.iterrows():
        value = '('
        for item in row:
            value += f"'{item}',"
        value = value.rstrip(',') + '),'
        values.append(value)
    insert_into_query += ''.join(values).rstrip(',') + ';'
    
    # Connect to MySQL database and execute the queries
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            cursor.execute(insert_into_query)
            connection.commit()
            print(f"Table {table_name} created and data inserted successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    csv_file_path = input("Enter the CSV file path: ")
    table_name = input("Enter the table name: ")
    host = input("Enter MySQL host: ")
    database = input("Enter MySQL database: ")
    user = input("Enter MySQL user: ")
    password = input("Enter MySQL password: ")
    
    csv_to_sql(csv_file_path, table_name, host, database, user, password)

