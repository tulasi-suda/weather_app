import os

class Config:
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        
        # API key
        self.API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        self.REQUEST_TIMEOUT = 10
        
        # Database Configuration
        self.DB_PATH = 'weather_data.db'
        self.LOG_FILE = 'weather_log.json'
        
        self.REQUESTS_PER_MINUTE = 50
    
    def validate_api_key(self):
        if not self.API_KEY:
            print(" OpenWeatherMap API key not found!")
            print(" Please set API key:")
            print("   - Export: export OPENWEATHER_API_KEY='weather_app/README.md'")
            print("   - Or get a free key from: https://openweathermap.org/api")
            return False
        return True
    
    def display_config(self):
        print("\n Application Configuration:")
        print(f"   API Key: {' Set' if self.API_KEY else ' Missing'}")
        print(f"   Database: {self.DB_PATH}")
        print(f"   Log File: {self.LOG_FILE}")
        print(f"   Rate Limit: {self.REQUESTS_PER_MINUTE} requests/minute")