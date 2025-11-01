import os
import mysql.connector
import csv
import uuid
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")


def connect_db():
    """Connect to MySQL server"""
    # Create a connection to the MySQL server
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
    )
    return conn


def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()


def connect_to_prodev():
    """Connect to ALX_prodev database"""
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="ALX_prodev"
    )
    return conn


def create_table(connection):
    """Create user_data table if it doesn't exist"""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) Primary Key,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    cursor.close()


def insert_data(connection, data):
    """Insert data from CSV file into user_data table"""
    cursor = connection.cursor()
    # Open the CSV file and read its contents
    with open(data, newline='', encoding='utf-8') as f:
        # Use csv.DictReader to read the CSV file
        reader = csv.DictReader(f)

        # Iterate over each row in the CSV file
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]

            # Insert the data into the user_data table
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
    # Commit the data to the database
    connection.commit()
    cursor.close()