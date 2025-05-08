DROP DATABASE IF EXISTS weather_data;
CREATE DATABASE weather_data;

\c weather_data;

DROP TABLE IF EXISTS weather_data;
DROP TABLE IF EXISTS air_quality_data;

SET TIMEZONE = 'Asia/Ho_Chi_Minh';

CREATE TABLE weather_data (
    datetime TIMESTAMPTZ PRIMARY KEY,
    temperature NUMERIC,
    feels_like NUMERIC,
    humidity NUMERIC,
    pressure NUMERIC,
    visibility NUMERIC,
    wind_speed NUMERIC
);


CREATE TABLE air_quality_data (
    datetime TIMESTAMPTZ PRIMARY KEY,
    co NUMERIC,
    no NUMERIC,
    no2 NUMERIC,
    o3 NUMERIC,
    so2 NUMERIC,
    pm2_5 NUMERIC,
    pm10 NUMERIC,
    nh3 NUMERIC
);
