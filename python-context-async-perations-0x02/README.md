# Python Context Managers and Asynchronous Database Operations

This project demonstrates how to build custom context managers and perform asynchronous database operations using Python. It is part of the `alx-backend-python` program and is designed to simulate real-world database handling scenarios efficiently and cleanly.

## 🚀 Learning Objectives

- Understand and implement class-based custom context managers using `__enter__()` and `__exit__()`.
- Build reusable context managers to manage database connections and queries.
- Perform asynchronous database operations using `aiosqlite`.
- Use `asyncio.gather()` to run queries concurrently and improve performance.

## 📁 Project Structure

- `0-databaseconnection.py`: Custom context manager for handling DB connections.
- `1-execute.py`: Context manager that takes a query and executes it.
- `3-concurrent.py`: Asynchronous functions that perform concurrent database queries using `asyncio` and `aiosqlite`.

## 🛠 Requirements

- Python 3.8+
- SQLite3
- `aiosqlite` (install with `pip install aiosqlite`)
