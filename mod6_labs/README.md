# Weather Application - Module 6 Lab

## Student Information
- **Name**: C-jay Lavapie
- **Student ID**: 221001254
- **Course**: CCCS 106
- **Section**: B

## Project Overview
This is a small desktop weather application built with Flet and Python. It fetches current weather and a 5-day forecast from OpenWeatherMap and presents the results with a modern, responsive UI. The app includes a search history, a theme toggle (light/dark), and a Google-like search layout where the search input is centered on top and the `Get Weather` button is centered below it.

## Features Implemented

### Base Features
- City search functionality (enter a city and press Enter or click `Get Weather`)
- Current weather display (temperature, feels-like, humidity, wind speed)
- Weather icons (provided by OpenWeatherMap)
- Error handling and user feedback
- Modern Material-like UI built with Flet

### Enhanced Features
- Persistent search history: the last searches are saved to `search_history.json` and shown when the search field is focused.
- 5-day forecast view: grouped by day and presented as tabs with daily high/low and a representative weather icon.
- Google-like search layout: wide centered input on top, with the centered `Get Weather` button below.
- Theme toggle: switch between light and dark modes from the top-right of the app.
- Robust history handling: corrupted `search_history.json` files are backed up automatically to a `.bak` file and reset.

## Screenshots
Include screenshots of the following (place image files in `assets/` and reference them here if desired):
- Main search screen with the input and centered `Get Weather` button
- Current weather result card
- 5-day forecast tabs
- Search history panel open

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Setup Instructions (Windows / PowerShell)
Run these commands from a PowerShell prompt inside the `mod6_labs` folder.

```powershell
# Create virtual environment
python -m venv venv
# Activate the venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your API key (OPENWEATHER_API_KEY)
# Example (create file .env and add this line):
# OPENWEATHER_API_KEY=your_api_key_here
```

Note: `config.py` expects the environment variable `OPENWEATHER_API_KEY`. If it's missing the app will raise a helpful error.

## Running the App
With the virtual environment activated, run:

```powershell
python main.py
```

The app window should open. Type a city name and press Enter or click `Get Weather`.

## Project Structure
- `main.py` - Flet UI and app logic
- `weather_service.py` - Async HTTP client to call OpenWeatherMap (current + forecast endpoints)
- `config.py` - Loads configuration (API key, app dimensions, units)
- `requirements.txt` - Python dependencies
- `search_history.json` - (auto-created) stores recent searches

## Troubleshooting
- Config/API key errors: Ensure `.env` contains `OPENWEATHER_API_KEY` and you activated the virtual environment before running.
- Corrupted history file: If `search_history.json` becomes unreadable, the app will rename it to `search_history.bak` and continue with an empty history.
- UI or layout issues: The app uses Flet; verify your installed `flet` version matches `requirements.txt` (`flet==0.28.3`).

## Development Notes
- Asynchronous design: `httpx.AsyncClient` and `asyncio` are used for non-blocking network calls; Flet's `page.run_task` schedules background coroutines.
- UI details: The search input is intentionally wide (`width=600`) to emulate a Google-like search box; the `Get Weather` button is centered underneath.

## Credits
- Built for CCCS 106 Module 6
- Icons and weather imagery via OpenWeatherMap

## License
This project is for educational use. Feel free to reuse the code for learning purposes.

---

## Screenshots of Features
![alt text](<screenshots/Adaptive UI.png>)
![alt text](<screenshots/Location Based.png>)
![alt text](<screenshots/Search History.png>)
![alt text](<screenshots/Temperature Toggle.png>)