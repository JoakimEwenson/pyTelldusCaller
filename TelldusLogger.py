from TelldusCaller import fetchSensorList, fetchSensorData
from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up SQLAlchemy
Engine = create_engine('sqlite:///sensordata.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=Engine)

class SensorDataRow(Base):
    __tablename__ = 'sensordata'

    id = Column(Integer, primary_key=True)
    sensorid = Column(String)
    clientName = Column(String)
    name = Column(String)
    lastUpdated = Column(String)
    ignored = Column(Boolean)
    editable = Column(Boolean)
    tempValue = Column(Float)
    tempLastUpdated = Column(String)
    tempMaxValue = Column(Float)
    tempMaxTime = Column(String)
    tempMinValue = Column(Float)
    tempMinTime = Column(String)
    humidityValue = Column(Float)
    humidityLastUpdated = Column(String)
    humidityMaxValue = Column(Float)
    humidityMaxTime = Column(String)
    humidityMinValue = Column(Float)
    humidityMinTime = Column(String)
    timezoneOffset = Column(String)

session = Session()

# Fetch sensor data
result = fetchSensorList()

for r in result:
    row = SensorDataRow(
        sensorid=r.sensorid,
        clientName=r.clientName,
        name=r.name,
        lastUpdated=r.lastUpdated,
        ignored=r.ignored,
        editable=r.editable,
        tempValue=r.tempValue,
        tempLastUpdated=r.tempLastUpdated,
        tempMaxValue=r.tempMaxValue,
        tempMaxTime=r.tempMaxTime,
        tempMinValue=r.tempMinValue,
        humidityValue=r.humidityValue,
        humidityLastUpdated=r.humidityLastUpdated,
        humidityMaxValue=r.humidityMaxValue,
        humidityMaxTime=r.humidityMaxTime,
        humidityMinValue=r.humidityMinValue,
        humidityMinTime=r.humidityMinTime,
        timezoneOffset=r.timezoneOffset,
    )
    session.add(row)

session.commit()
    