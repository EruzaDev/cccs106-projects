# User Login System – Week 3 Lab

## Student Information
- **Name**: C-jay Lavapie
- **Student ID**: 221001254
- **Course**: CCCS 106
- **Section**: B

## Project Overview
A simple user login system built with **Flet** and **MySQL**. Users can log in with credentials stored in a MySQL database. The app features a modern, frameless window design with success/failure dialogs.

## Features
- User authentication against MySQL database
- Frameless window with centered layout
- Success and failure alert dialogs
- Input validation (empty field check)
- Database error handling

## Project Structure
```
week3_labs/
├── src/
│   ├── main.py          # Flet UI and login logic
│   ├── db_connection.py # MySQL connection helper
│   └── assets/          # App assets
├── pyproject.toml       # Project configuration
└── README.md
```

## Prerequisites
- Python 3.8+
- MySQL Server running locally
- A database with a `users` table containing `username` and `password` columns

## Installation

```powershell
cd week3_labs

# Install dependencies (using pip or poetry)
pip install flet mysql-connector-python

# Or with Poetry
poetry install
```

## Database Setup
Create a MySQL database and table:

```sql
CREATE DATABASE IF NOT EXISTS cccs106_db;
USE cccs106_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'password123');
```

Update `db_connection.py` with your MySQL credentials.

## Running the App

```powershell
cd src
python main.py
```

Or with Flet CLI:
```powershell
flet run
```

## Build for Distribution

```powershell
# Windows
flet build windows -v

# Android
flet build apk -v
```

For more build options, see the [Flet Packaging Guide](https://flet.dev/docs/publish/).

## License
Educational use for CCCS 106 coursework.