import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List

class DataLogger:
    
    def __init__(self, config):
        self.config = config
        self._init_database()
    
    def _init_database(self):
        try:
            conn = sqlite3.connect(self.config.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    country TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    feels_like REAL NOT NULL,
                    humidity INTEGER NOT NULL,
                    pressure INTEGER NOT NULL,
                    weather_condition TEXT NOT NULL,
                    wind_speed REAL NOT NULL,
                    visibility TEXT,
                    api_timestamp TEXT NOT NULL,
                    query_timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_city_time 
                ON weather_data(city, query_timestamp)
            ''')
            
            conn.commit()
            conn.close()
            
            print(f" Database initialized: {self.config.DB_PATH}")
            
        except sqlite3.Error as e:
            print(f" Database error: {e}")
    
    def log_to_database(self, weather_data: Dict) -> bool:
        """
        Log weather data to SQLite database
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.config.DB_PATH)
            cursor = conn.cursor()
            
            # Insert weather data
            cursor.execute('''
                INSERT INTO weather_data 
                (city, country, temperature, feels_like, humidity, pressure,
                 weather_condition, wind_speed, visibility, api_timestamp, query_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                weather_data['city'],
                weather_data['country'],
                weather_data['temperature'],
                weather_data['feels_like'],
                weather_data['humidity'],
                weather_data['pressure'],
                weather_data['weather_condition'],
                weather_data['wind_speed'],
                str(weather_data['visibility']),
                weather_data['api_timestamp'],
                weather_data['timestamp']
            ))
            
            conn.commit()
            conn.close()
            
            print(f" Data logged to database for {weather_data['city']}")
            return True
            
        except sqlite3.Error as e:
            print(f" Database logging error: {e}")
            return False
    
    def log_to_file(self, weather_data: Dict) -> bool:
        """
        Log weather data to JSON file
        Creates human-readable log with timestamps
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create log entry with metadata
            log_entry = {
                'log_timestamp': datetime.now().isoformat(),
                'weather_data': weather_data
            }
            
            # Read existing logs or create new list
            logs = []
            if os.path.exists(self.config.LOG_FILE):
                try:
                    with open(self.config.LOG_FILE, 'r') as f:
                        logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []  # Start fresh if file is corrupted
            
            # Add new log entry
            logs.append(log_entry)
            
            # Write back to file
            with open(self.config.LOG_FILE, 'w') as f:
                json.dump(logs, f, indent=2)
            
            print(f" Data logged to file for {weather_data['city']}")
            return True
            
        except Exception as e:
            print(f" File logging error: {e}")
            return False
    
    def get_recent_queries(self, limit: int = 5) -> List[Dict]:
        """
        Get recent weather queries from database
        
        Args:
            limit: Number of recent queries to retrieve
            
        Returns:
            List of recent weather data
        """
        try:
            conn = sqlite3.connect(self.config.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT city, temperature, humidity, weather_condition, query_timestamp
                FROM weather_data 
                ORDER BY query_timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            # Convert to list of dictionaries
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            conn.close()
            return results
            
        except sqlite3.Error as e:
            print(f" Error reading from database: {e}")
            return []
    
    def display_recent_queries(self):
        """
        Display recent weather queries in a formatted way
        """
        recent_queries = self.get_recent_queries(5)
        
        if not recent_queries:
            print("\n No recent queries found.")
            return
        
        print(f"\n LAST {len(recent_queries)} WEATHER QUERIES")
        print("="*60)
        
        for i, query in enumerate(recent_queries, 1):
            time_str = query['query_timestamp'][11:16]  # Extract time only
            print(f"{i}. {query['city']}")
            print(f"     {query['temperature']}°C |  {query['humidity']}%")
            print(f"    {query['weather_condition']}")
            print(f"    {time_str}")
            print("-" * 60)