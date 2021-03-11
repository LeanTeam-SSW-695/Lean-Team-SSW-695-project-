"""
    authors: 
    Abdulellah Shahrani, Chengyi Zhang, Haoran Li, and Sachin Paramesha
    the code:
    a program that uses the US Census geocoding API to retrieve the
    location (latitude and longitude) of two addresses,
    and compute the approximate distance, in miles, between the two locations.
"""

import urllib.request, urllib.error, urllib.parse
import json
import math
import requests


def read_address(address):
    """ a function that takes a one line address and return the latitude and longitude
        of that address
    """

    global js
    geocoding_api = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?'
    parms = dict()
    parms['address'], parms['benchmark'], parms['format'] = address, 'Public_AR_Current', 'json'

    url = geocoding_api + urllib.parse.urlencode(parms)

    uh = urllib.request.urlopen(url)
    data = uh.read().decode()

    js = json.loads(data)

    coordinates = dict()

    coordinates['x'] = js['result']['addressMatches'][0]['coordinates']['x']
    coordinates['y'] = js['result']['addressMatches'][0]['coordinates']['y']

    return coordinates


def distance(user_address_1, user_address_2):
    """ a function that return the distance in miles """

    x1, y1 = user_address_1['x'], user_address_1['y']
    x2, y2 = user_address_2['x'], user_address_2['y']

    radius = 3956

    dx = math.radians(x2 - x1)
    dy = math.radians(y2 - y1)

    a = math.sin(dx / 2) * math.sin(dx / 2) + math.cos(math.radians(x1)) \
        * math.cos(math.radians(x2)) * math.sin(dy / 2) * math.sin(dy / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = radius * c

    return d

def the_weather(user_weather_1, user_weather_2):
    """ a function to retrieve the current temperature of both addresses using the OpenWeatherMap API"""

    x1, y1 = user_weather_1['y'], user_weather_1['x']
    x2, y2 = user_weather_2['y'], user_weather_2['x']

    api_key = "7a160b5068bd8bad7f789b5e9b450a69"
    url_1 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (x1, y1, api_key)
    url_2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (x2, y2, api_key)

    response_1 = requests.get(url_1)
    response_2 = requests.get(url_2)

    data_1 = json.loads(response_1.text)
    data_2 = json.loads(response_2.text)

    current_temp_1 = data_1["current"]["temp"]
    current_temp_2 = data_2["current"]["temp"]

    return current_temp_1, current_temp_2


def main(address_1, address_2):

    user_address_1 = read_address(address_1)
    user_address_2 = read_address(address_2)

    the_distance = distance(user_address_1, user_address_2)

    user_weather_1 = user_address_1
    user_weather_2 = user_address_2
    weather_1, weather_2 = the_weather(user_weather_1, user_weather_2)
    
    return round(the_distance, 2)

