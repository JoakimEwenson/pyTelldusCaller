from TelldusCaller import fetchSensorList, fetchSensorData
from os import path
from sqlite3 import Error
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

    return conn

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
        c.execute(f"INSERT INTO sensordata(sensorid,clientName,name,lastUpdated,tempValue,tempLastUpdated,tempMaxValue,tempMaxTime,tempMinValue,tempMinTime,humidityValue,humidityLastUpdated,humidityMaxValue,humidityMaxTime,humidityMinValue,humidityMinTime,timezoneOffset) VALUES('{row.sensorid}','{row.clientName}','{row.name}','{row.lastUpdated}','{row.tempValue}','{row.tempLastUpdated}','{row.tempMaxValue}','{row.tempMaxTime}','{row.tempMinValue}','{row.tempMinTime}','{row.humidityValue}','{row.humidityLastUpdated}','{row.humidityMaxValue}','{row.humidityMaxTime}','{row.humidityMinValue}','{row.humidityMinTime}','{row.timezoneOffset}')")
        conn.commit()

def first_run():
    conn = create_connection(db_file)
    if conn is not None:
        create_table(conn, sql_create_sensordata_table)
    else:
        print('Error, could not connect to database')

if __name__ == '__main__':
    if (path.exists(db_file) == False):
        first_run()
    else:
        conn = create_connection(db_file)

    # Fetch sensor data
    result = fetchSensorList(True)
    insert_sensordata(conn, result)