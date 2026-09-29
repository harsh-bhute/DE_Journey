# Weather Data ETL Pipeline

## What the project does
This project fetches current weather data from a weather API,
transforms the required fields into a clean format with appropriate
data types, and loads the processed data into a SQLite database.

The pipeline follows:
Extract → Transform → Load (ETL)

## Technologies Used
- Python
- Requests
- Pandas
- SQLite
- Python Logging

## How to Run
Run the project from the terminal using:

python Project1.py

The script can also be imported and executed as a Python module.

## Output
The processed weather data is stored in the SQLite database
`weather.db` in the `weather_snapshots` table.

Example output:

FeelsLikeC  temp_C  weatherDesc  humidity  windspeedKmph  fetched_at
32          28      Clear        77        16             2026-09-29 19:10:46
32          28      Clear        77        16             2026-09-29 19:06:41
32          28      Sunny        77        19             2026-09-29 16:59:16