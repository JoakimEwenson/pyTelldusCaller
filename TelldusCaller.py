import json
import requests
from datetime import datetime
from settings import telldus_user

# Base URL for the API
base_url = "https://pa-api.telldus.com/json"

'''
 SensorObject with default data in case of empty or invalid response.
 Note that last_updated-values of all sorts are a Unix timestamp and might 
 need some adjusting to display correct values.
'''


class SensorObject():
    sensor_id = 0
    client_name = ''
    name = ''
    last_updated = ''
    ignored = 0
    editable = 0
    temp_value = None
    temp_last_updated = None
    temp_max_value = None
    temp_max_time = None
    temp_min_value = None
    temp_min_time = None
    humidity_value = None
    humidity_last_updated = None
    humidity_max_value = None
    humidity_max_time = None
    humidity_min_value = None
    humidity_min_time = None
    timezone_offset = 0


''' 
 Function for collecting a list of sensors connected to your Telldus account and fetch latest available information from them.
 This function returns a list of SensorObjects to the user.
'''


def fetch_sensor_list(return_raw=False):
    telldus_url = '{}/sensors/list'.format(base_url)
    telldus_call = telldus_user.get(telldus_url)
    result = json.loads(telldus_call.text)
    sensor_list = []
    for res in result['sensor']:
        if (return_raw):
            sensor_list.append(fetch_sensor_data(res['id'], True))
        else:
            sensor_list.append(fetch_sensor_data(res['id']))

    return sensor_list


'''
 Function for collecting the latest available information from a specified Telldus sensor ID.
 Returns a SensorObject containing the information to the user
'''


def fetch_sensor_data(sensor_id, return_raw=False):
    telldus_url = '{}/sensor/info?id={}'.format(base_url, sensor_id)

    telldus_call = telldus_user.get(telldus_url)

    json_data = json.loads(telldus_call.text)

    if json_data:
        result = SensorObject()
        result.sensor_id = json_data['id']
        result.name = json_data['name']
        result.client_name = json_data['clientName']
        result.last_updated = json_data['lastUpdated'] if return_raw else datetime.fromtimestamp(
            int(json_data['lastUpdated']))
        try:
            if json_data['data'][0]['name'] == 'temp':
                # Handle temperature values
                result.temp_value = float(json_data['data'][0]['value'])
                result.temp_max_value = float(json_data['data'][0]['max'])
                result.temp_min_value = float(json_data['data'][0]['min'])
                # Handle datetime values
                if (return_raw):
                    result.temp_last_updated = json_data['data'][0]['lastUpdated']
                    result.temp_max_time = json_data['data'][0]['maxTime']
                    result.temp_min_time = json_data['data'][0]['minTime']
                else:
                    result.templast_updated = datetime.fromtimestamp(
                        int(json_data['data'][0]['lastUpdated']))
                    result.temp_max_time = datetime.fromtimestamp(
                        int(json_data['data'][0]['maxTime']))
                    result.temp_min_time = datetime.fromtimestamp(
                        int(json_data['data'][0]['minTime']))
        except Exception:
            pass
        try:
            if json_data['data'][1]['name'] == 'humidity':
                # Handle humidity values
                result.humidity_value = int(json_data['data'][1]['value'])
                result.humidity_max_value = int(json_data['data'][1]['max'])
                result.humidity_min_value = int(json_data['data'][1]['min'])
                # Handle datetime values
                if (return_raw):
                    result.humidity_last_updated = json_data['data'][1]['lastUpdated']
                    result.humidity_max_time = json_data['data'][1]['maxTime']
                    result.humidity_min_time = json_data['data'][1]['minTime']
                else:
                    result.humidity_last_updated = datetime.fromtimestamp(
                        int(json_data['data'][1]['lastUpdated']))
                    result.humidity_max_time = datetime.fromtimestamp(
                        int(json_data['data'][1]['maxTime']))
                    result.humidity_min_time = datetime.fromtimestamp(
                        int(json_data['data'][1]['minTime']))
        except Exception:
            pass
        result.timezone_offset = json_data['timezoneoffset']

    else:
        result = SensorObject()

    return result


'''
 If file run as standalone, return sample data to user
'''
if __name__ == '__main__':
    result = fetch_sensor_list()
    for res in result:
        print()
        print(f'{res.client_name} - {res.name}')
        if res.temp_value:
            print(
                f'Temperature: {res.temp_value}\u00b0C at {res.templast_updated}')
        if res.humidity_value:
            print(
                f'Humidity: {res.humidity_value}% at {res.humidity_last_updated}')
        print()
