import requests
import logging
import pandas as pd
import sqlite3


logging.basicConfig(
    filename="Project1.log",
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s  - %(message)s'
)

def fetch_weather():
    try:
        logging.info("Pipeline started")
        response = requests.get('https://wttr.in/Mumbai?format=j1',timeout=10)
        response.raise_for_status()
        logging.info("Request Successful")


    except requests.exceptions.ConnectionError:
        logging.exception(f"Connection failed")
        return
    except requests.exceptions.HTTPError as e:
        logging.exception(f"HTTP error: {e}")
        return
    except requests.exceptions.RequestException as e:
        logging.exception(f"Request failed:{e}")
        return

    Weather_data = response.json()
    return Weather_data

#This steps are to check the data to parse, in this way we will find the hierarchy 
# #print(Weather_data)

# print(type(Weather_data))
# Weather_data.keys()
# type(Weather_data["current_condition"])

# Weather_data["current_condition"][0].keys()

# FeelsLikeC = Weather_data["current_condition"][0]["FeelsLikeC"]
# temp_C = Weather_data["current_condition"][0]["temp_C"]
# weatherDesc = Weather_data["current_condition"][0]["weatherDesc"][0]["value"]
# humidity = Weather_data["current_condition"][0]["humidity"]
# windspeedKmph = Weather_data["current_condition"][0]["windspeedKmph"]

# type(Weather_data["current_condition"][0]["temp_C"])

def transform_weather_data(Weather_data):
    data = {
        "FeelsLikeC" : [Weather_data["current_condition"][0]["FeelsLikeC"]],
        "temp_C" : [Weather_data["current_condition"][0]["temp_C"]],
        "weatherDesc" : [Weather_data["current_condition"][0]["weatherDesc"][0]["value"]],
        "humidity" : [Weather_data["current_condition"][0]["humidity"]],
        "windspeedKmph" : [Weather_data["current_condition"][0]["windspeedKmph"]],
        }

    df = pd.DataFrame(data)

    df["fetched_at"] = pd.Timestamp.now()

    df = df.astype({"FeelsLikeC":"int","temp_C":"int","humidity":"int","windspeedKmph":"int"})
    return df


def load_to_db(df):
    conn = None
    try:
        conn = sqlite3.connect('weather.db')
        logging.info("Connecion to DB successful")

        df.to_sql('weather_snapshots',
                conn,
                if_exists='append',
                index= False
                )
        conn.commit()
        result = pd.read_sql("SELECT * FROM weather_snapshots ORDER BY fetched_at DESC LIMIT 5", conn)
        logging.info(f"\n{result.to_string()}")
        print(result)
    except sqlite3.Error as e:
        logging.exception(f"Error while loading{e}")
    finally:
        if conn is not None:
            conn.close()

def main():
    Weather_data = fetch_weather()
    if Weather_data is None:
        return

    df = transform_weather_data(Weather_data)
    load_to_db(df)
    logging.info("Pipeline Completed Successfully")

if __name__ == "__main__":
    main()




#To clear the database

# conn = sqlite3.connect('weather.db')
# cursor = conn.cursor()
# cursor.execute("DELETE FROM weather_snapshots")
# conn.commit()
# # rows = cursor.fetchall()
# # print(rows)
