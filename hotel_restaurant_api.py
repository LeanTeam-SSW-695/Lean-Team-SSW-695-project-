import json
import requests
from amadeus import Client, ResponseError

def find_restaurant(location, term = "food", rating = 4.0, page = 1):
    """
    The function search term around location and show reviews
    Location: The location
    Term: The food type you want to search, default is food
    Rating: Display the result above the rating, default is 4
    Page: The page displayed, each page have 5 result, default is 1
    """
    api_key = "zmG2CEc6FuS1WgkRP7kX1mUwv78J6uQQ-MiazaqvxMoqdbGrdzDBhtUndsI7WTOorz2aUcOs-NOTeEa7120RkNZ3qy6M0xRsQr3nHpraT6m5SvK2H0P8NlK3WS1bYHYx"
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': term, 'location': location}

    req = requests.get(url, params = params, headers = headers)
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]

    list = []
    count = 0
    for business in businesses:
        bdic = {}
        if rating <= float(business["rating"]):
            if count // 5 + 1 == page:
                bdic["Name"] = business["name"]
                bdic["Rating"] = business["rating"]
                bdic["Address"] = " ".join(business["location"]["display_address"])
                bdic["Phone"] = business["phone"]
                count += 1

                id = business["id"]
                url="https://api.yelp.com/v3/businesses/" + id + "/reviews"
                req = requests.get(url, headers = headers)
                parsed = json.loads(req.text)
                reviews = parsed["reviews"]

                bdic["Review"] = {}
                for review in reviews:
                    bdic["Review"]["User"] = review["user"]["name"]
                    bdic["Review"]["Rating"] = review["rating"]
                    bdic["Review"]["Text"] = review["text"]

                list.append(bdic)
    return list

def print_restaurant(location, term = "food", rating = 4.0, page = 1):
    print(json.dumps(find_restaurant(location, term = "food", rating = 4.0, page = 1), indent=4))

def find_hotel(city, page = 1):
    """
    Find hotels by city
    City: The city
    Page: The page displayed, each page have 5 result, default is 1
    """
    amadeus = Client(
        client_id='zfkFUCVDPnvzLZbeQ9POHk0xwgKDEtgl',      #api_key
        client_secret='SiN9lW5mXrzDLP83'                   #api_secret
    )

    hotels_by_city = amadeus.shopping.hotel_offers.get(cityCode = city)
    hlist = []
    count = 0
    for item in hotels_by_city.data:
        hdic = {}
        if count // 5 + 1 == page:                            #each page has five hotels
            print(item["hotel"]["name"])
            hdic["Name"] = item["hotel"]["name"]
            hdic["Address"] = item["hotel"]["address"]["lines"][0] + ", " + item["hotel"]["address"]["cityName"] +             ", " + item["hotel"]["address"]["stateCode"] + ", " + item["hotel"]["address"]["postalCode"]
            hdic["Contact"] = item["hotel"]["contact"]["phone"]
            hdic["Offers"] = []
            for room in item["offers"]:
                rdic = {}
                try:
                    rdic["Type"] = str(room["room"]["typeEstimated"]["beds"]) + " " +                     room["room"]["typeEstimated"]["bedType"] + " BED"
                except KeyError:
                    rdic["Type"] = str(room["room"]["typeEstimated"])
                rdic["Price"] = room["price"]["total"]
                hdic["Offers"].append(rdic)
            hlist.append(hdic)
        elif count // 5 + 1 > page:
            break
        print(count)
        count += 1

    return hlist

def print_hotel(city, page = 1):
    print(json.dumps(find_hotel(city, page), indent=4))
