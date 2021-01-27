from TelldusCaller import fetch_sensor_list, fetch_sensor_data
from os import path
from sqlite3 import Error
from datetime import datetime
import time
import sqlite3
import os.path

db_file = 'sensordata.db'

sql_create_sensordata_table = """ CREATE TABLE IF NOT EXISTS sensordata (
                                    id integer PRIMARY KEY,
                                    sensorid integer NOT NULL,
                                    clientName text,
                                    name text,
                                    lastUpdated text,
                                    tempValue real,
                                    tempLastUpdated text,
                                    tempMaxValue real,
                                    tempMaxTime text,
                                    tempMinValue real,
                                    tempMinTime text,
                                    humidityValue real,
                                    humidityLastUpdated text,
                                    humidityMaxValue real,
                                    humidityMaxTime text,
                                    humidityMinValue real,
                                    humidityMinTime text,
                                    timezoneOffset integer
                                ); """


def create_connection(db_file):
    """ Create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None


def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_sensordata(conn, data):
    c = conn.cursor()
    for row in data:
        c.execute(
            f"INSERT INTO sensordata(sensorid,clientName,name,lastUpdated,tempValue,tempLastUpdated,tempMaxValue,tempMaxTime,tempMinValue,tempMinTime,humidityValue,humidityLastUpdated,humidityMaxValue,humidityMaxTime,humidityMinValue,humidityMinTime,timezoneOffset) VALUES('{row.sensor_id}','{row.client_name}','{row.name}','{row.last_updated}','{row.temp_value}','{row.temp_last_updated}','{row.temp_max_value}','{row.temp_max_time}','{row.temp_min_value}','{row.temp_min_time}','{row.humidity_value}','{row.humidity_last_updated}','{row.humidity_max_value}','{row.humidity_max_time}','{row.humidity_min_value}','{row.humidity_min_time}','{row.timezone_offset}')")
        conn.commit()


if __name__ == '__main__':
    if (path.exists(db_file) == False):
        conn = create_connection(db_file)
        if conn is not None:
            create_table(conn, sql_create_sensordata_table)
        else:
            print('Error, could not connect to database')
    else:
        conn = create_connection(db_file)

    # Fetch sensor data
    while True:
        try:
            result = fetch_sensor_list(True)
            insert_sensordata(conn, result)
            print(f"Successful fetch at {datetime.now()}")
        except Error as error:
            print(error)
        # Sleep for 60 s and try again
        time.sleep(300)
