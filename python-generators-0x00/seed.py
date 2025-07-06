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
            password=""  # 🔁 Replace with your real MySQL root password
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
            password="",  # 🔁 Replace this too as necessary
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

def insert_data(connection, filename):
    try:
        cursor = connection.cursor()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())  # generate a UUID
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
        cursor.close()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Failed to insert data: {e}")

