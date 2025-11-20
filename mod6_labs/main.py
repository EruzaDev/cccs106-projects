"""Weather Application using Flet v0.28.3"""

import json
from pathlib import Path
import asyncio
import httpx
import flet as ft
from weather_service import WeatherService
from config import Config


class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        self.current_unit = "metric"  # Default to Celsius
        self.current_temp = None
        self.current_feels_like = None
        self.current_weather_data = None
        self.setup_page()
        self.build_ui()
        # Auto-fetch location weather on startup
        self.page.run_task(self.get_current_location_weather)
    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE,
        )
        
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()
    
    def build_ui(self):
        """Build the user interface."""
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )
        
        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
        )

        # Unit toggle button (C/F)
        self.unit_button = ft.IconButton(
            icon=ft.Icons.THERMOSTAT,
            tooltip="Toggle °C/°F",
            on_click=self.toggle_units,
        )

        # Current location button
        self.location_button = ft.IconButton(
            icon=ft.Icons.MY_LOCATION,
            tooltip="Use my location",
            on_click=lambda e: self.page.run_task(self.get_current_location_weather),
        )

        # Title row with buttons
        title_row = ft.Row(
            [
                self.title,
                ft.Row([
                    self.location_button,
                    self.unit_button,
                    self.theme_button,
                ]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Search button (placed ABOVE input field)
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )

        # Centered button row
        button_row = ft.Row(
            [
                ft.Container(content=self.search_button, width=200),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            width=600,
            on_focus=self.show_history,
            on_blur=self.hide_history,
            on_submit=self.on_search,
        )

        # Search history dropdown (positioned below input)
        self.history_dropdown = ft.Container(
            visible=False,
            border_radius=ft.border_radius.only(
                bottom_left=8,
                bottom_right=8,
                top_left=0,
                top_right=0
            ),
            padding=0,
            width=600,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            content=ft.Column([], spacing=0),
        )

        # Weather display container (initially hidden)
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
        )
        
        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
        )
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)

        # Add all components to page
        self.page.add(
            ft.Column(
                [
                    title_row,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    button_row,  # Button first
                    ft.Column(
                        [
                            self.city_input,
                            self.history_dropdown,  # Dropdown right after input
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    async def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.run_task(self.get_weather)
    
    async def get_weather(self):
        """Fetch and display weather data."""
        city = self.city_input.value.strip()
        
        if not city:
            self.show_error("Please enter a city name")
            return
        
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()
        
        try:
            # Fetch weather with city only, units handled by weather_service
            weather_data = await self.weather_service.get_weather(city)
            self.current_weather_data = weather_data
            self.current_temp = weather_data.get("main", {}).get("temp", 0)
            self.current_feels_like = weather_data.get("main", {}).get("feels_like", 0)
            
            await self.display_weather(weather_data)
            
        except Exception as e:
            self.show_error(str(e))
        
        finally:
            self.loading.visible = False
            self.add_to_history(city)
            self.page.update()
    
    async def display_weather(self, data: dict):
        """Display weather information with dynamic styling."""
        self.weather_container.animate_opacity = 300
        self.weather_container.opacity = 0
        self.weather_container.visible = True
        self.page.update()

        await asyncio.sleep(0.1)
        self.weather_container.opacity = 1
        
        # Extract data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # Dynamic background color based on weather
        weather_main = data.get("weather", [{}])[0].get("main", "").lower()
        bg_color, emoji = self.get_weather_styling(weather_main)
        
        # Unit symbol
        unit_symbol = "°C" if self.current_unit == "metric" else "°F"
        
        # Build weather display
        self.weather_container.bgcolor = bg_color
        self.weather_container.content = ft.Column(
            [
                ft.Text(
                    f"{city_name}, {country}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Column([
                            ft.Text(emoji, size=40),
                            ft.Text(
                                description,
                                size=20,
                                italic=True,
                            ),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                ft.Text(
                    f"{temp:.1f}{unit_symbol}",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Text(
                    f"Feels like {feels_like:.1f}{unit_symbol}",
                    size=16,
                    color=ft.Colors.GREY_700,
                ),
                
                ft.Divider(),
                
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind Speed",
                            f"{wind_speed} m/s"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()
    
    def get_weather_styling(self, weather_main: str):
        """Get background color and emoji based on weather condition."""
        styles = {
            "clear": (ft.Colors.AMBER_100, "☀️"),
            "clouds": (ft.Colors.BLUE_GREY_100, "☁️"),
            "rain": (ft.Colors.BLUE_100, "🌧️"),
            "drizzle": (ft.Colors.LIGHT_BLUE_100, "🌦️"),
            "thunderstorm": (ft.Colors.INDIGO_100, "⛈️"),
            "snow": (ft.Colors.BLUE_50, "❄️"),
            "mist": (ft.Colors.GREY_100, "🌫️"),
            "fog": (ft.Colors.GREY_100, "🌫️"),
            "haze": (ft.Colors.GREY_100, "🌫️"),
        }
        return styles.get(weather_main, (ft.Colors.BLUE_50, "🌤️"))
    
    def create_info_card(self, icon, label, value):
        """Create an info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=150,
        )
    
    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()

    def toggle_theme(self, e):
        """Toggle between light and dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()

    def toggle_units(self, e):
        """Toggle between Celsius and Fahrenheit."""
        if self.current_unit == "metric":
            self.current_unit = "imperial"
        else:
            self.current_unit = "metric"
        
        # If we have current weather data, convert and redisplay
        if self.current_weather_data and self.current_temp is not None:
            self.convert_temperature()
            self.page.run_task(self.redisplay_weather)

    def convert_temperature(self):
        """Convert stored temperatures between units."""
        if self.current_unit == "imperial":
            # Convert from Celsius to Fahrenheit
            self.current_temp = (self.current_temp * 9/5) + 32
            self.current_feels_like = (self.current_feels_like * 9/5) + 32
        else:
            # Convert from Fahrenheit to Celsius
            self.current_temp = (self.current_temp - 32) * 5/9
            self.current_feels_like = (self.current_feels_like - 32) * 5/9

    async def redisplay_weather(self):
        """Redisplay weather with converted temperature."""
        if not self.current_weather_data:
            return
        
        # Update the temperature values in the data
        self.current_weather_data["main"]["temp"] = self.current_temp
        self.current_weather_data["main"]["feels_like"] = self.current_feels_like
        
        await self.display_weather(self.current_weather_data)

    async def get_current_location_weather(self):
        """Get weather for current location using IP."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://ipapi.co/json/")
                data = response.json()
                city = data.get('city', '')
                
                if city:
                    self.city_input.value = city
                    await self.get_weather()
        except Exception as e:
            self.show_error("Could not detect your location")

    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                try:
                    backup = self.history_file.with_suffix('.bak')
                    self.history_file.replace(backup)
                except Exception:
                    try:
                        self.history_file.unlink()
                    except Exception:
                        pass
                return []
            except Exception:
                return []
        return []
    
    def save_history(self):
        """Save search history to file."""
        try:
            if self.history_file.parent and not self.history_file.parent.exists():
                self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving search history: {e}")
    
    def add_to_history(self, city: str):
        """Add city to history."""
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:10]
            self.save_history()

    def show_history(self, e):
        """Show search history when the city input is focused."""
        if not self.search_history:
            return

        items = []
        for city in self.search_history:
            items.append(
                ft.Container(
                    content=ft.Text(city, size=14),
                    padding=10,
                    on_click=lambda e, c=city: self.select_history_item(c),
                    ink=True,
                )
            )
        
        self.history_dropdown.content.controls = items
        self.history_dropdown.visible = True
        self.page.update()

    def hide_history(self, e):
        """Hide dropdown when textfield loses focus."""
        self.page.run_task(self._delayed_hide)

    async def _delayed_hide(self):
        await asyncio.sleep(0.15)
        self.history_dropdown.visible = False
        self.page.update()

    def select_history_item(self, city: str):
        """Fill textfield when user clicks a history item."""
        self.city_input.value = city
        self.history_dropdown.visible = False
        self.page.update()
        self.page.run_task(self.get_weather)


def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)