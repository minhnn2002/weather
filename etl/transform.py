import pandas as pd
import json
import sys
from config import Config
from utils import setup_logger

logger = setup_logger(__name__)

def read_weather_data(file_name = "weather_data.json"):
    # Read data from json file and return
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data["days"]
    except FileNotFoundError:
        logger.error(f"File {file_name} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from the file.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")

def transform_weather_data(weather_data):
    # Extract relevant attributes
    weather_df = []
    for day in weather_data:
        for hour in day['hours']:
            hour['date'] = day['datetime']  
            weather_df.append(hour)

    weather_df = pd.DataFrame(weather_df)
    weather_df = weather_df[["datetimeEpoch", "temp", "feelslike", "humidity", "pressure", "visibility", "windspeed"]]
    weather_df.columns = ["datetime", "temperature", "feels_like", "humidity", "pressure", "visibility", "wind_speed"]

    # Convert data types
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"], unit = "s")
    start = pd.Timestamp('2025-01-01 00:00:00')
    end = pd.Timestamp('2025-01-30 23:00:00')
    weather_df = weather_df[(weather_df['datetime'] >= start) & (weather_df['datetime'] <= end)]

    # Handle missing values
    weather_df.ffill(inplace=True)
    weather_df.dropna(inplace=True)

    return weather_df



def read_air_quality_data(file_name = "air_quality_data.json"):
    # Read data from json file and return
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data["list"]
    except FileNotFoundError:
        logger.error(f"File {file_name} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from the file.")
        sys.exit(1)


def transform_air_quality_data(air_quality_data):
    # Extract relevant attributes
    air_quality_df = pd.json_normalize(air_quality_data)
    air_quality_df = air_quality_df.drop(columns=["main.aqi"])
    air_quality_df.rename(columns={
            "dt": "datetime"
        },
        inplace=True
    )
    air_quality_df.columns = [col.replace("components.", "") for col in air_quality_df.columns]
    
    # Convert data types
    air_quality_df["datetime"] = pd.to_datetime(air_quality_df["datetime"], unit="s")
    start = pd.Timestamp('2025-01-01 00:00:00')
    end = pd.Timestamp('2025-01-30 23:00:00')
    air_quality_df = air_quality_df[(air_quality_df['datetime'] >= start) & (air_quality_df['datetime'] <= end)]

    # Handle missing values
    air_quality_df.ffill(inplace=True)
    air_quality_df.dropna(inplace=True)

    return air_quality_df


def main():
    # Weather data
    logger.info("Tranform the weather data")
    weather_data = read_weather_data()
    transformed_weather_data = transform_weather_data(weather_data)
    logger.info("Save to to transformed_weather_data.csv")
    transformed_weather_data.to_csv("transformed_weather_data.csv", index=False)

    # Air quality data
    logger.info("Tranform the air_quality data")
    air_quality_data = read_air_quality_data()
    transformed_air_quality_data = transform_air_quality_data(air_quality_data)
    logger.info("Save to to transformed_weather_data.csv")
    transformed_air_quality_data.to_csv("transformed_air_quality_data.csv", index=False)

if __name__ == "__main__":
    main()






