import json
import requests
from datetime import datetime
from settings import telldus_user

# Base URL for the API
base_url = "https://api.telldus.com/json"

'''
 SensorObject with default data in case of empty or invalid response.
 Note that LastUpdated-values of all sorts are a Unix timestamp and might 
 need some adjusting to display correct values.
'''
class SensorObject():
    sensorid = 0
    clientName = ''
    name = ''
    lastUpdated = ''
    ignored = 0
    editable = 0
    tempValue = None
    tempLastUpdated = None
    tempMaxValue = None
    tempMaxTime = None
    tempMinValue = None
    tempMinTime = None
    humidityValue = None
    humidityLastUpdated = None
    humidityMaxValue = None
    humidityMaxTime = None
    humidityMinValue = None
    humidityMinTime = None
    timezoneOffset = 0


''' 
 Function for collecting a list of sensors connected to your Telldus account and fetch latest available information from them.
 This function returns a list of SensorObjects to the user.
'''
def fetchSensorList(returnRaw=False):
    telldus_url = '{}/sensors/list'.format(base_url)
    telldus_call = telldus_user.get(telldus_url)
    result = json.loads(telldus_call.text)
    sensor_list = []
    for res in result['sensor']:
        if (returnRaw):
            sensor_list.append(fetchSensorData(res['id'],True))
        else:
            sensor_list.append(fetchSensorData(res['id']))

    return sensor_list

'''
 Function for collecting the latest available information from a specified Telldus sensor ID.
 Returns a SensorObject containing the information to the user
'''
def fetchSensorData(sensorId, returnRaw=False):
    telldus_url = '{}/sensor/info?id={}'.format(base_url, sensorId)

    telldus_call = telldus_user.get(telldus_url)

    jsonData = json.loads(telldus_call.text)
    if jsonData:
        result = SensorObject()
        result.sensorid = jsonData['id']
        result.name = jsonData['name']
        result.clientName = jsonData['clientName']
        result.lastUpdated = jsonData['lastUpdated'] if returnRaw else datetime.fromtimestamp(int(jsonData['lastUpdated']))
        try:
            if jsonData['data'][0]['name'] == 'temp':
                # Handle temperature values
                result.tempValue = float(jsonData['data'][0]['value'])
                result.tempMaxValue = float(jsonData['data'][0]['max'])
                result.tempMinValue = float(jsonData['data'][0]['min'])
                # Handle datetime values
                if (returnRaw):
                    result.tempLastUpdated = jsonData['data'][0]['lastUpdated']
                    result.tempMaxTime = jsonData['data'][0]['maxTime']
                    result.tempMinTime = jsonData['data'][0]['minTime']
                else:
                    result.tempLastUpdated = datetime.fromtimestamp(int(jsonData['data'][0]['lastUpdated']))
                    result.tempMaxTime = datetime.fromtimestamp(int(jsonData['data'][0]['maxTime']))
                    result.tempMinTime = datetime.fromtimestamp(int(jsonData['data'][0]['minTime']))
        except:
            pass
        try:
            if jsonData['data'][1]['name'] == 'humidity':
                # Handle humidity values
                result.humidityValue = int(jsonData['data'][1]['value'])
                result.humidityMaxValue = int(jsonData['data'][1]['max'])
                result.humidityMinValue = int(jsonData['data'][1]['min'])
                # Handle datetime values
                if (returnRaw):
                    result.humidityLastUpdated = jsonData['data'][1]['lastUpdated']
                    result.humidityMaxTime = jsonData['data'][1]['maxTime']
                    result.humidityMinTime = jsonData['data'][1]['minTime']
                else:
                    result.humidityLastUpdated = datetime.fromtimestamp(int(jsonData['data'][1]['lastUpdated']))
                    result.humidityMaxTime = datetime.fromtimestamp(int(jsonData['data'][1]['maxTime']))
                    result.humidityMinTime = datetime.fromtimestamp(int(jsonData['data'][1]['minTime']))
        except:
            pass
        result.timezoneOffset = jsonData['timezoneoffset']

    else:
        result = SensorObject()

    return result

'''
 If file run as standalone, return sample data to user
'''
if __name__ == '__main__':
    result = fetchSensorList()
    for res in result:
        print()
        print(f'{res.clientName} - {res.name}')
        if res.tempValue:
            print(f'Temperature: {res.tempValue}\u00b0C at {res.tempLastUpdated}')
        if res.humidityValue:
            print(f'Humidity: {res.humidityValue}% at {res.humidityLastUpdated}')
        print()