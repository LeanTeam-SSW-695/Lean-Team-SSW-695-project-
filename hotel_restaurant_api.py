import json
import requests
import main

def find_restaurant(address, term = "food", rating = 4.0, miles = 5, number = 5):
    """
    The function search term around location and show reviews
    address: The address
    Term: The food type you want to search, default is food
    Rating: Display the result above the rating, default is 4
    Page: The page displayed, each page have 5 result, default is 1
    """
    api_key = "zmG2CEc6FuS1WgkRP7kX1mUwv78J6uQQ-MiazaqvxMoqdbGrdzDBhtUndsI7WTOorz2aUcOs-NOTeEa7120RkNZ3qy6M0xRsQr3nHpraT6m5SvK2H0P8NlK3WS1bYHYx"
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': term, 'location': address}

    req = requests.get(url, params = params, headers = headers)
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]

    user_address = main.read_address(address)
    list = []
    count = 0
    for business in businesses:
        bdic = {}
        res_address = main.read_address(" ".join(business["location"]["display_address"]))
        dis = main.distance(user_address, res_address)
        if rating <= float(business["rating"]):
            if float(dis[0].split(" ")[0]) < miles:
                bdic["Name"] = business["name"]
                bdic["Rating"] = business["rating"]
                bdic["Address"] = " ".join(business["location"]["display_address"])
                bdic["Phone"] = business["phone"]
                count += 1

#                 id = business["id"]
#                 url="https://api.yelp.com/v3/businesses/" + id + "/reviews"
#                 req = requests.get(url, headers = headers)
#                 parsed = json.loads(req.text)
#                 reviews = parsed["reviews"]

#                 bdic["Review"] = {}
#                 for review in reviews:
#                     bdic["Review"]["User"] = review["user"]["name"]
#                     bdic["Review"]["Rating"] = review["rating"]
#                     bdic["Review"]["Text"] = review["text"]
#                     break

                list.append(bdic)

            if count >= number:
                break
    return list

def print_restaurant(address, term = "food", rating = 4.0, miles = 5, number = 5):
    print(json.dumps(find_restaurant(address, term, rating, miles, number), indent=4))

def find_hotel(address, miles = 5, number = 5):
    """
    Find hotels by city
    City: The address
    Page: The page displayed, each page have 5 result, default is 1
    """
    api_key = 'AIzaSyBGMcgUxRVurcyByfLrnRlOyI_cKdvMkiE'
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    r = requests.get(url + 'query=hotel in ' + address +
                        '&key=' + api_key)
    result = r.json()
    hotels = result['results']

    user_address = main.read_address(address)
    hlist = []
    count = 0

    for hotel in hotels:
        hdic = {}
        hotel_address = main.read_address(hotel["formatted_address"])
        dis = main.distance(user_address, hotel_address)
        if float(dis[0].split(" ")[0]) < miles:
            hdic["Name"] = hotel["name"]
            hdic["Address"] = hotel["formatted_address"]
            try:
                hdic["Open"] = hotel["opening_hours"]["open_now"]
            except KeyError:
                hdic["Open"] = "Unknown"
            hdic["Rating"] = hotel["rating"]
            hlist.append(hdic)
            count += 1
        if count > number:
            break

    return hlist

def print_hotel(address, miles = 5, number = 5):
    print(json.dumps(find_hotel(address, miles, number), indent=4))
