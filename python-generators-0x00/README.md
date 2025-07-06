# Python Generators – Task 0: Getting Started with Python Generators

## 🧠 Project Overview

This project explores advanced usage of Python generators to efficiently handle large datasets, simulate real-time data processing, and optimize memory usage. The project is tightly integrated with SQL databases (MySQL), where we fetch and process data using Python generators in a performant, lazy-loading style.

---

## ✅ Task 0: Database Seeding

### Objective

Create a Python script that:

- Connects to a MySQL server
- Creates a database (`ALX_prodev`) if it doesn’t exist
- Creates a table (`user_data`) with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR)
  - `email` (VARCHAR)
  - `age` (DECIMAL)
- Inserts user records from a CSV file (`user_data.csv`) if they do not already exist

---

## 🛠️ Files

| Filename     | Description                               |
|--------------|-------------------------------------------|
| `seed.py`    | Handles database connection, table creation, and data insertion |
| `0-main.py`  | Sample driver script to execute the `seed.py` logic |
| `user_data.csv` | Sample user data for seeding the `user_data` table |

---

## 📦 Sample Output

```text
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('uuid', 'name', 'email', age), ...]

🔧 Setup Requirements

    Python 3.x

    MySQL server installed and running

    mysql-connector-python library

Install dependency:

pip install mysql-connector-python

🔐 Notes

    The script avoids inserting duplicate entries by checking for existing user_id.
