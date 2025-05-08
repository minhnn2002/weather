import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WEATHER_KEY = os.getenv("WEATHER_KEY")
    AIR_KEY = os.getenv("AIR_KEY")

    PG_HOST = os.getenv("PG_HOST")
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_DB = os.getenv("PG_DB")

