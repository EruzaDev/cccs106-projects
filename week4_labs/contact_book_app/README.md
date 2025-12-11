# Contact Book App – Week 4 Lab

## Student Information
- **Name**: C-jay Lavapie
- **Student ID**: 221001254
- **Course**: CCCS 106
- **Section**: B

## Project Overview
A contact management application built with **Flet** and **SQLite**. Users can add, edit, delete, and search contacts. The app features circular initial avatars with a 5-color palette and a modern dark/light theme toggle.

## Features
- **CRUD Operations**: Add, view, edit, and delete contacts
- **Search**: Filter contacts in real-time
- **Circular Avatars**: Display contact initials with deterministic colors from a 5-color palette
- **Country Code Selection**: Dropdown with common country prefixes
- **Email Validation**: Auto-append `@gmail.com` if no domain; validates domain format
- **Theme Toggle**: Switch between dark and light modes
- **SQLite Database**: Persistent local storage in `src/contacts.db`

## Project Structure
```
contact_book_app/
├── src/
│   ├── main.py        # Flet UI entry point
│   ├── app_logic.py   # Contact display, add, edit, delete logic
│   ├── database.py    # SQLite initialization and helpers
│   ├── utils/         # Validation, country prefixes, avatar colors
│   ├── contacts.db    # SQLite database (auto-created)
│   └── assets/        # App assets
├── pyproject.toml     # Project configuration
└── README.md
```

## Installation

```powershell
cd week4_labs/contact_book_app

# Install with pip
pip install flet

# Or with Poetry
poetry install
```

## Running the App

```powershell
cd src
python main.py
```

Or with Flet CLI:
```powershell
flet run
```

## Usage
1. Enter a contact's **Name**, **Phone** (with country code), and **Email**
2. Click **Add Contact** to save
3. Use the search box to filter contacts
4. Click a contact to edit or delete
5. Toggle dark/light mode with the switch in the header

## Build for Distribution

```powershell
# Windows
flet build windows -v

# Android
flet build apk -v

# Web
flet run --web
```

For more build options, see the [Flet Packaging Guide](https://flet.dev/docs/publish/).

## License
Educational use for CCCS 106 coursework.