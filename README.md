# weather_app
##  Real-Time Weather Info & Logger
## Overview
This Python application fetches real-time weather data from OpenWeatherMap API for user-specified cities and logs all responses with timestamps to both SQLite database and text files .Designed with Object-Oriented Programming (OOP) principles to keep code organized and maintainable. Proper error handling ensures robustness against invalid city names or API issues.
## Project Structure
WEATHER ├── config.py ├── requirements.txt ├── weather_fetcher.py └──data_logger.py  |---main.py
## Features
- Input city names interactively or type exit to quit.
- Fetches live temperature (in °C), humidity (%), and weather conditions.
-	Displays simple meaningful explanations about temperature and humidity values.
-	Logs each lookup response into a SQLite database with a timestamp.
-	Uses OOP with clear separation of concerns: fetching data, displaying info, and logging.
-	Handles invalid inputs and API errors gracefully.
## Requirements
Python 3.6+

requests library
## Installation
1.Clone or download the project files

2.Install required dependencies:

        pip install requests
        
3.Get an API key from OpenWeatherMap
     Sign up for a free account
     Generate an API key in your dashboard
## Database Schema
The SQLite database weather_logs.db contains one table named weather_data with the following fields:

Column  	Type	  Description

id INTEGER	   Auto-increment primary key

city  TEXT	  Name of the city

temperature	REAL	Temperature in Celsius

humidity	INTEGER	Humidity percentage

conditions	TEXT	Weather condition description (e.g., clear sky)

timestamp 	TEXT  	Date and time when data was logged

## Error Handling
-	If the city name is empty, the program prompts for a valid name.
-	If the API request fails (network issues or invalid city), an error message is displayed.
-	Unexpected API response formats are caught and notified to the user.
-	Database connection problems.

## Example of Data base
1️ Get weather for a city

2️ View all weather logs

3️ View statistics (visualization)

4️ Clear all logs

5️ Exit

 Enter your choice: 1
 
 Enter city name: kavali
 
 WEATHER REPORT FOR Kāvali
 
Temperature: 25.28°C

 Humidity: 66%
 
 Pressure: 1012 hPa
 
 Wind Speed: 4.95 m/s
 
 Conditions: Overcast Clouds
 
 Time: 2025-11-28 16:52:51
 
