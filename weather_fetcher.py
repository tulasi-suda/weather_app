import requests
import time
from datetime import datetime
from typing import Dict, Optional, Tuple


class WeatherFetcher:
    def __init__(self, config):
        self.config = config
        self._last_request_time = 0
        self._request_interval = 60 / self.config.REQUESTS_PER_MINUTE

    def _rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self._request_interval:
            sleep_time = self._request_interval - time_since_last_request
            print(f" Rate limiting: waiting {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        self._last_request_time = time.time()

    def _validate_city_name(self, city_name: str) -> Tuple[bool, str]:
        if not city_name:
            return False, 
        if not isinstance(city_name, str):
            return False, 
        cleaned_city = city_name.strip()
        if not cleaned_city:
            return False, 
        dangerous_chars = [';', '"', "'", '\\', '/', '|']
        if any(char in city_name for char in dangerous_chars):
            return False, 

        return True, ""

    def _make_api_request(self, city_name: str) -> Optional[Dict]:
        try:
            params = {
                'q': city_name,
                'appid': self.config.API_KEY,
                'units': 'metric',
                'lang': 'en'
            }

            response = requests.get(
                self.config.BASE_URL,
                params=params,
                timeout=self.config.REQUEST_TIMEOUT
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            print(f"Request timeout for '{city_name}'. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            print(" Connection error. Please check your internet connection.")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print(" Invalid API key. Please check your OPENWEATHER_API_KEY.")
            elif e.response.status_code == 404:
                print(f" City '{city_name}' not found. Please check the spelling.")
            elif e.response.status_code == 429:
                print(" API rate limit exceeded. Please wait a minute.")
            else:
                print(f" HTTP error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f" Request failed: {e}")
            return None

    def _parse_weather_data(self, api_data: Dict, city_name: str) -> Optional[Dict]:
        try:
            main_data = api_data['main']
            weather_data = api_data['weather'][0]
            wind_data = api_data.get('wind', {})
            sys_data = api_data['sys']

            weather_info = {
                'city': api_data['name'],
                'country': sys_data['country'],
                'temperature': main_data['temp'],
                'feels_like': main_data['feels_like'],
                'humidity': main_data['humidity'],
                'pressure': main_data['pressure'],
                'weather_condition': weather_data['description'].title(),
                'weather_main': weather_data['main'],
                'wind_speed': wind_data.get('speed', 0),
                'visibility': api_data.get('visibility', 'N/A'),
                'timestamp': datetime.now().isoformat(),
                'api_timestamp': datetime.fromtimestamp(api_data['dt']).isoformat()
            }

            return weather_info

        except KeyError as e:
            print(f" Error parsing weather data for '{city_name}': Missing field {e}")
            return None
        except Exception as e:
            print(f" Unexpected error parsing data for '{city_name}': {e}")
            return None

    def get_weather(self, city_name: str) -> Optional[Dict]:
        print(f"\n Searching for weather in: {city_name}")

        is_valid, error_message = self._validate_city_name(city_name)
        if not is_valid:
            print(f" Validation error: {error_message}")
            return None

        self._rate_limit()
        api_data = self._make_api_request(city_name)
        if not api_data:
            return None

        return self._parse_weather_data(api_data, city_name)

    def display_weather(self, weather_data: Dict) -> None:
        if not weather_data:
            print(" No weather data to display.")
            return

        emoji = self._get_weather_emoji(weather_data['weather_main'])

        print("\n" + "=" * 50)
        print(f"{emoji} WEATHER FOR {weather_data['city']}, {weather_data['country']}")
        print("=" * 50)
        print(f" Temperature: {weather_data['temperature']}°C")
        print(f" Feels like: {weather_data['feels_like']}°C")
        print(f" Humidity: {weather_data['humidity']}%")
        print(f" Pressure: {weather_data['pressure']} hPa")
        print(f" Conditions: {weather_data['weather_condition']}")
        print(f" Wind Speed: {weather_data['wind_speed']} m/s")

        if weather_data['visibility'] != 'N/A':
            visibility_km = weather_data['visibility'] / 1000
            print(f" Visibility: {visibility_km:.1f} km")

        print(f" Updated: {weather_data['api_timestamp'][11:16]} UTC")
        print("=" * 50)

    def _get_weather_emoji(self, weather_main: str) -> str:
        emoji_map = {
            'Clear': '',
            'Clouds': '',
            'Rain': '',
            'Drizzle': '',
            'Thunderstorm': '',
            'Snow': '',
            'Mist': '',
            'Fog': ''
        }
        return emoji_map.get(weather_main, '')
