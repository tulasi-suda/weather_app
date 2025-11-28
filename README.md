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

```
Column  Type  Description

id INTEGER  Auto-increment primary key

city  TEXT  Name of the city

temperature REAL Temperature in Celsius

humidity INTEGER Humidity percentage

conditions TEXT	Weather condition description (e.g., clear sky)

timestamp TEXT  Date and time when data was logged
```

## Error Handling
-	If the city name is empty, the program prompts for a valid name.
-	If the API request fails (network issues or invalid city), an error message is displayed.
-	Unexpected API response formats are caught and notified to the user.
-	Database connection problems.

## Example of Data base
```
WEATHER APPLICATION MENU

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

 1️ Get weather for a city

2️ View all weather logs

3️ View statistics (visualization)

4️ Clear all logs

5️ Exit

 Enter your choice: 2
```
 
 ## Final output
 ```
 WEATHER LOGS:
 
================================================================================

 2025-11-27 23:08:28 | Guntur |  20.54°C |  79.0% |  Broken Clouds  
 
 2025-11-27 23:08:35 | Ponnur |  22.2°C |  78.0% |  Overcast Clouds 
 
 2025-11-27 23:08:47 | Chīrāla |  23.06°C |  74.0% |  Overcast Clouds
 
 2025-11-27 23:08:54 | Bāpatla |  22.78°C |  73.0% |  Overcast Clouds
 
 2025-11-27 23:09:03 | Tirumala - Tirupati |  18.19°C |  85.0% |  Overcast Clouds
 
 2025-11-27 23:09:09 | Tirumala |  16.17°C |  87.0% |  Overcast Clouds
 
 2025-11-27 23:09:14 | Gao |  29.34°C |  12.0% |  Overcast Clouds 
 
 2025-11-27 23:09:21 | Vijayawada |  20.78°C |  75.0% |  Broken Clouds
 
 2025-11-27 23:25:35 | Ongole |  23.32°C |  73.0% |  Overcast Clouds
 
 2025-11-27 23:25:45 | Nellore |  23.09°C |  75.0% |  Overcast Clouds
 
 2025-11-28 16:52:51 | Kāvali |  25.28°C |  66.0% |  Overcast Clouds
 
 2025-11-28 16:53:13 | Nandigāma |  26.78°C |  54.0% |  Broken Clouds


 WEATHER APPLICATION MENU
 
1️  Get weather for a city

2️  View all weather logs

3️  View statistics (visualization)

4️  Clear all logs

5️  Exit
 Enter your choice: 3


 WEATHER APPLICATION MENU
 
1️  Get weather for a city

2️  View all weather logs

3️  View statistics (visualization)

4️  Clear all logs

5️  Exit

 Enter your choice: 5
 
 Exiting... Goodbye.
```
 
