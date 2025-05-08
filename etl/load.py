import pandas as pd
from sqlalchemy import create_engine
import sys
from config import Config
from utils import setup_logger

logger = setup_logger(__name__)


def create_db_engine():
    """
        Create engine to db
    """
    try:
        user = Config.PG_USER
        password = Config.PG_PASSWORD
        host = Config.PG_HOST
        dbname = Config.PG_DB
        URL = f"postgresql+psycopg2://{user}:{password}@{host}:5432/{dbname}"
        engine = create_engine(URL)

        return engine
    except Exception as e:
        logger.error(f"Error creating database engine: {e}")
        sys.exit(1)


def load_data_to_sql(file_name, table_name, engine):
    """
        Load data to db
    """
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        logger.error("Error: File not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logger.error("Error:File is empty.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info(f"Data loaded into the table {table_name} successfully!")
    except Exception as e:
        logger.error(f"Error loading data to PostgreSQL: {e}")
        sys.exit(1)


def main():
    engine = create_db_engine()

    # Load weather data
    logger.info("Load weather data to db")
    load_data_to_sql(
        file_name="transformed_weather_data.csv",
        table_name="weather_data",
        engine=engine
    )

    # Load air quality data
    logger.info("Load air quality data to db")
    load_data_to_sql(
        file_name="transformed_air_quality_data.csv",
        table_name="air_quality_data",
        engine=engine
    )


if __name__ == "__main__":
    main()
