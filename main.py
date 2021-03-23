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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time


def get_location():
    options = Options()
    options.add_argument("--use--fake-ui-for-media-stream")
    driver = webdriver.Chrome(executable_path='/Users/abod/Desktop/SSW 695/LeanTeam-SSW-695/chromedriver',
                              options=options)
    timeout = 10
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(3)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = str(longitude[0])
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])
    neighborhood = driver.find_elements_by_xpath('//*[@id="neighborhood"]')
    neighborhood = [x.text for x in neighborhood]
    neighborhood = str(neighborhood[0])
    driver.quit()

    coordinates = dict()
    coordinates['lat'] = latitude
    coordinates['lng'] = longitude
    coordinates['neighborhood'] = neighborhood

    return coordinates



def read_address(address):
    """ a function that takes a one line address and return the latitude and longitude
        of that address
    """

    apiKey = "AIzaSyDNOv-Nu97S_HcvAl7j4OqLsjsesmf-5TI"
    geocoding_api = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = urllib.parse.urlencode({"address": address, "key": apiKey})
    url = f"{geocoding_api}?{params}"

    result = json.load(urllib.request.urlopen(url))
    coordinates = dict()
    coordinates['lat'] = result['results'][0]['geometry']['location']['lat']
    coordinates['lng'] = result['results'][0]['geometry']['location']['lng']

    if result["status"] in ["OK", "ZERO_RESULTS"]:
        return coordinates

    raise Exception(result["error_message"])


def distance(user_address_1, user_address_2):
    """ a function that return the distance in miles """

    originCoor = "%s,%s" % (user_address_1['lat'], user_address_1['lng'])
    destinCoor = "%s,%s" % (user_address_2['lat'], user_address_2['lng'])
    api_key = "AIzaSyDNOv-Nu97S_HcvAl7j4OqLsjsesmf-5TI"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}" \
        .format(originCoor, destinCoor, api_key)

    response = requests.get(url)

    data = json.loads(response.text)
    ''' = data["rows"]["elements"]["duration"]["text"]'''
    if data["status"] in ["OK"]:
        routeDistance = data['rows'][0]['elements'][0]['distance']['text']
        routeDuration = data['rows'][0]['elements'][0]['duration']['text']
        return routeDistance, routeDuration
    elif data["status"] in ["ZERO_RESULTS"]:
        raise Exception(data['status'])
    else:
        raise Exception(data["error_message"])


def the_weather(user_weather_1, user_weather_2):
    """ a function to retrieve the current temperature of both addresses using the OpenWeatherMap API"""

    x1, y1 = user_weather_1['lat'], user_weather_1['lng']
    x2, y2 = user_weather_2['lat'], user_weather_2['lng']

    api_key = "7a160b5068bd8bad7f789b5e9b450a69"
    url_1 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (x1, y1, api_key)
    url_2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (x2, y2, api_key)

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

    the_distance, the_duration = distance(user_address_1, user_address_2)

    user_weather_1 = user_address_1
    user_weather_2 = user_address_2
    weather_1, weather_2 = the_weather(user_weather_1, user_weather_2)

    return the_distance, the_duration, weather_1, weather_2
