import requests
import json
import logging
import sys
from datetime import datetime, timezone
from config import Config
from utils import setup_logger

logger = setup_logger(__name__)


def get_weather_data(start, end, location = 'hanoi'):
    """
    Fetch weather data for a specific location and date range from Visual Crossing API

    Parameter:
        location(str): location where the weather data is fetched
        start(str): the start date in yyyy-mm-dd format
        end(str): the end date in yyyy-mm-dd format

    Return:
        dict: weather data
    """

    URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start}/{end}"
    logging.info(URL)
    try:
        response = requests.get(
            URL,
            params = {
                "key": Config.WEATHER_KEY,
                "include": "hours"
            }
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        sys.exit(1)

def get_air_quality_data(start, end, lat = 21.0285, long = 105.8542):
    """
    Fetch historical air quality data for a given location and date range from the AirVisual API.

    Parameters:
        lat (str): The latitude of the location.
        long (str): The longtitude of the location.
        start (str): The start date in YYYY-MM-DD format.
        end (str): The end date in YYYY-MM-DD format.

    Returns:
        dict: The air quality data as a Python dictionary.
    """
    URL = f"http://api.openweathermap.org/data/2.5/air_pollution/history"
    try:
        response = requests.get(
            URL,
            params={
                "lat": lat,
                "lon": long,
                "start": int(datetime.strptime(start, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).timestamp()),
                "end": int(datetime.strptime(end, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).timestamp()),
                "appid": Config.AIR_KEY
            }
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        sys.exit(1)

def main():
    start = "2025-01-01T00:00:00"
    end = "2025-01-31T23:00:00"

    logger.info(f"Fetching weather data for 'Ha Noi' from {start} to {end}...")
    weather_data = get_weather_data(start, end)

    logger.info(f"Fetching historical air quality data for 'Ha Noi', from {start} to {end}...")
    air_quality_data = get_air_quality_data(start, end)

    # Save the raw data to a file
    with open("weather_data.json", "w") as file:
        json.dump(weather_data, file, indent=4)
    logger.info("Weather data saved to weather_data.json")

    with open("air_quality_data.json", "w") as file:
        json.dump(air_quality_data, file, indent=4)
    logger.info("Air quality data saved to historical_air_quality_data.json")

if __name__ == "__main__":
    main()