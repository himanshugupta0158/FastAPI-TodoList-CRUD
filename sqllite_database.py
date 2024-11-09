import sqlite3
from sqlite3 import Error

class SQLiteDatabase:
    def __init__(self, db_file):
        """Initialize a new or connect to an existing database."""
        self.db_file = db_file
        self.connection = self.create_connection()

    def create_connection(self):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(f"Connected to SQLite database: {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")
        return conn

    def create_table_from_schema(self, table_name, schema):
        """
        Create a table using a dictionary-based schema definition.
        :param table_name: Name of the table to be created.
        :param schema: Dictionary where keys are column names and values are data types.
        """
        columns = ', '.join([f"{col_name} {col_type}" for col_name, col_type in schema.items()])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            print(f"Table '{table_name}' created successfully.")
        except Error as e:
            print(f"Error creating table '{table_name}': {e}")

    def fetch_all_data(self, table_name):
        """fetch all data from the specified table."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error retrieving data: {e}")
            return []

    def insert(self, table, data):
        """Insert a new row into the specified table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, tuple(data.values()))
            self.connection.commit()
            print("Record inserted successfully.")
        except Error as e:
            print(f"Error inserting data: {e}")

    def update(self, table, data, condition):
        """Update a record in the specified table based on the given condition."""
        updates = ', '.join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table} SET {updates} WHERE {condition}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, tuple(data.values()))
            self.connection.commit()
            print("Record updated successfully.")
        except Error as e:
            print(f"Error updating data: {e}")

    def delete(self, table, condition):
        """Delete records from the specified table based on the given condition."""
        sql = f"DELETE FROM {table} WHERE {condition}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            self.connection.commit()
            print("Record(s) deleted successfully.")
        except Error as e:
            print(f"Error deleting data: {e}")

    def select(self, query, params=None):
        """Execute a SELECT query and return the results."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error retrieving data: {e}")
            return []

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("SQLite connection closed.")

# Usage example
if __name__ == "__main__":
    # Initialize the database
    db = SQLiteDatabase("example.db")

    # Define table schema as a dictionary
    user_schema = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "age": "INTEGER",
        "gender": "TEXT"
    }

    # Create table using the schema dictionary
    db.create_table_from_schema("users", user_schema)

    # Insert a new record
    db.insert("users", {"name": "Alice", "age": 25, "gender": "female"})

    # Update a record
    db.update("users", {"age": 26}, "name = 'Alice'")

    # Select all records
    users = db.select("SELECT * FROM users")
    print("Users:", users)

    # Delete a record
    db.delete("users", "name = 'Alice'")

    # Close the connection
    db.close_connection()
