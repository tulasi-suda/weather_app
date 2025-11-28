import requests
import sqlite3
import time
from datetime import datetime
import matplotlib.pyplot as plt

class Config:
    API_KEY = "fdf5cdc14d37e9c26d825894866ff174"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    DB_NAME = "weather_logs.db"
    REQUEST_TIMEOUT = 10
class DatabaseManager:
    def __init__(self, db_name=Config.DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        
        query = """
        CREATE TABLE IF NOT EXISTS weather_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            wind_speed REAL,
            weather_condition TEXT,
            timestamp TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_log(self, data):
        query = """
        INSERT INTO weather_logs (city, temperature, humidity, pressure, wind_speed, weather_condition, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        self.conn.execute(query, (
            data["city"],
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["wind_speed"],
            data["weather_condition"],
            data["timestamp"]
        ))
        self.conn.commit()

    def fetch_all_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM weather_logs")
        return cursor.fetchall()

    def clear_logs(self):
        self.conn.execute("DELETE FROM weather_logs")
        self.conn.commit()

    def close(self):
        self.conn.close()

class WeatherFetcher:
    def __init__(self, config: Config):
        self.config = config

    def get_weather(self, city_name: str):
        if not city_name.strip():
            print(" City name cannot be empty.")
            return None

        params = {
            'q': city_name,
            'appid': self.config.API_KEY,
            'units': 'metric',
            'lang': 'en'
        }

        try:
            response = requests.get(
                self.config.BASE_URL,
                params=params,
                timeout=self.config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return self._parse_weather_data(data)

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(" City not found. Please check the spelling.")
            elif response.status_code == 401:
                print(" Invalid API key. Please check your API key.")
            else:
                print(f" HTTP error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f" Network error: {e}")
            return None

    def _parse_weather_data(self, data):
        try:
            main = data["main"]
            wind = data["wind"]
            weather = data["weather"][0]

            parsed = {
                "city": data["name"],
                "temperature": main["temp"],
                "humidity": main["humidity"],
                "pressure": main["pressure"],
                "wind_speed": wind["speed"],
                "weather_condition": weather["description"].title(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return parsed
        except KeyError as e:
            print(f" Missing field in API response: {e}")
            return None

class WeatherApp:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.fetcher = WeatherFetcher(self.config)

    def menu(self):
        while True:
            print("\n WEATHER APPLICATION MENU ")
            print("1  Get weather for a city")
            print("2  View all weather logs")
            print("3  View statistics (visualization)")
            print("4  Clear all logs")
            print("5  Exit")

            choice = input(" Enter your choice: ").strip()

            if choice == '1':
                self.get_weather_for_city()
            elif choice == '2':
                self.view_logs()
            elif choice == '3':
                self.show_statistics()
            elif choice == '4':
                self.clear_logs()
            elif choice == '5':
                print(" Exiting... Goodbye!")
                self.db.close()
                break
            else:
                print(" Invalid choice. Please select from the menu.")

    def get_weather_for_city(self):
        city = input(" Enter city name: ").strip()
        data = self.fetcher.get_weather(city)
        if data:
            self.display_weather(data)
            self.db.insert_log(data)
        else:
            print(" Failed to fetch weather data.")

    def display_weather(self, data):
        print("\n" + "=" * 50)
        print(f" WEATHER REPORT FOR {data['city']}")
        print("=" * 50)
        print(f" Temperature: {data['temperature']}°C")
        print(f" Humidity: {data['humidity']}%")
        print(f" Pressure: {data['pressure']} hPa")
        print(f" Wind Speed: {data['wind_speed']} m/s")
        print(f" Conditions: {data['weather_condition']}")
        print(f" Time: {data['timestamp']}")
        print("=" * 50)

    def view_logs(self):
        logs = self.db.fetch_all_logs()
        if not logs:
            print(" No logs found.")
            return

        print("\n WEATHER LOGS:")
        print("=" * 80)
        for log in logs:
            print(f" {log[7]} | {log[1]} |  {log[2]}°C |  {log[3]}% |  {log[6]}")
        print("=" * 80)

    def show_statistics(self):
        logs = self.db.fetch_all_logs()
        if not logs:
            print(" No data available for statistics.")
            return

        cities = [log[1] for log in logs]
        temperatures = [log[2] for log in logs]
        humidities = [log[3] for log in logs]

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.bar(cities, temperatures, color='orange')
        plt.title("Average Temperature per City")
        plt.ylabel("Temperature (°C)")

        plt.subplot(2, 1, 2)
        plt.bar(cities, humidities, color='skyblue')
        plt.title("Humidity per City")
        plt.ylabel("Humidity (%)")

        plt.tight_layout()
        plt.show()

    def clear_logs(self):
        confirm = input(" Are you sure you want to delete all logs? (y/n): ").lower()
        if confirm == 'y':
            self.db.clear_logs()
            print(" All logs cleared successfully.")
        else:
            print(" Deletion cancelled.")

if __name__ == "__main__":
    app = WeatherApp()
    app.menu()
