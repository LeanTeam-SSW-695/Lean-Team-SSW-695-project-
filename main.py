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

    geocoding_api = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?'
    parms = dict()
    parms['address'], parms['benchmark'], parms['format'] = address, 'Public_AR_Current', 'json'

    try:
        url = geocoding_api + urllib.parse.urlencode(parms)

    except ValueError:
        print(f"The website you entered ({address}) has to start with http://")  # if the user entered a wrong website
    except urllib.error.HTTPError:
        print(f"HTTP Error 404: {address} Not Found")
    else:
        print('Retrieving', url)
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()

        try:
            js = json.loads(data)
        except:
            print('==== Failure To Retrieve ====')
            print(data)
            exit()

        coordinates = dict()

        try:
            coordinates['x'] = js['result']['addressMatches'][0]['coordinates']['x']
            coordinates['y'] = js['result']['addressMatches'][0]['coordinates']['y']

        except IndexError as i:
            print(i, '\nplease, make sure that you enter your one-line address correctly')

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


def main():
    address_1 = input('Enter the first address (must be a one line address): ')
    address_2 = input('Enter the second address (must be a one line address): ')

    user_address_1 = read_address(address_1)
    user_address_2 = read_address(address_2)

    the_distance = round(distance(user_address_1, user_address_2))

    print(f"The distance between the two addresses is about {the_distance} miles")

    
if __name__ == "__main__":
    main()
