#!/usr/bin/env python3
import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

def connect_db():
    """Connects to the MySQL server (not to a specific DB)"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # 🔁 Replace with your real MySQL root password
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace this too
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        """)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Inserts data from CSV file if not already in table"""
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row['user_id']
                # Check if user_id already exists
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
                if cursor.fetchone():
                    continue  # Skip duplicates
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_id,
                    row['name'],
                    row['email'],
                    row['age']
                ))
        connection.commit()
        print("Data inserted successfully (if not already present)")
    except Exception as e:
        print(f"Failed to insert data: {e}")
    finally:
        cursor.close()

