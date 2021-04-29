import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
import mysql.connector
from mysql.connector.constants import ClientFlag
import GoogleMapAPI
import hotel_restaurant_API
import GUI
import urllib.error

global username

def set_connection():
    config = {
        'user': 'root',
        'host': '35.220.246.119',
        'password': "12345678",
        'client_flags': [ClientFlag.SSL]
    }
    return config


class ScreenLoading(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.go_to_login, 2.5)

    def go_to_login(self, dt):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Login'


class ScreenLogin(Screen):
    def go_forward(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Start'

    def register(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Register'

    def login(self):
        if not self.login_(self.ids.username.text, self.ids.password.text):
            Factory.LoginFPop().open()
        else:
            Factory.LoginPop().open()
            global username
            username = self.ids.username.text
            self.go_forward()

    def login_(self, username, pwd):
        config = set_connection()
        config['database'] = 'login'  # add new database to config dict
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()  # initialize connection cursor
        query = "SELECT COUNT(*) FROM login WHERE Username = '" + username + "' AND Pwd = '" + pwd + "'"
        cursor.execute(query)
        out = cursor.fetchall()
        if out[0][0]:
            return True
        else:
            return False


class ScreenRegister(Screen):
    def go_forward(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Login'

    def Register(self):
        if self.register_(self.ids.username.text, self.ids.password.text):
            Factory.RegSuccessPop().open()
            self.go_forward()
        else:
            Factory.RegFailPop().open()

    def register_(self, username, pwd):
        config = set_connection()
        config['database'] = 'login'  # add new database to config dict
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()  # initialize connection cursor
        if self.login():
            print("User has registered!")
            return False
        cursor.execute("SELECT COUNT(*) FROM login WHERE Username = '" + username + "'")
        out = cursor.fetchall()
        if out[0][0]:
            print("Username has been used!")
        else:
            query = "INSERT INTO login (Username, Pwd) VALUES ('" + username + "', '" + pwd + "')"
            cursor.execute(query)
            cnxn.commit()  # and commit changes
            return True

    def login(self):
        config = set_connection()
        config['database'] = 'login'  # add new database to config dict
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()  # initialize connection cursor
        query = "SELECT COUNT(*) FROM login WHERE Username = '" + self.ids.username.text + "' AND Pwd = '" + self.ids.password.text + "'"
        cursor.execute(query)
        out = cursor.fetchall()
        if out[0][0]:
            return True
        else:
            return False


class ScreenOne(Screen):
    def go_forward(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Implement'

    def current_as_origin(self):
        coordinates = GoogleMapAPI.get_location()
        self.ids.Origin.text = coordinates['neighborhood']

    def current_as_destination(self):
        coordinates = GoogleMapAPI.get_location()
        self.ids.Destination.text = coordinates['neighborhood']

    def reset(self):
        self.ids.Origin.text = ""
        self.ids.Destination.text = ""

    def calc(self):
        global originAddress, destinationAddress
        originAddress = self.ids.Origin.text
        destinationAddress = self.ids.Destination.text
        try:
            global theDistance, theDuration
            theDistance, theDuration, originWeather, destinationWeather = GoogleMapAPI.main(originAddress,
                                                                                            destinationAddress)
            output = "Distance between origin and destination is about {}\n and the duration of the drive is {}." \
                     "\n\nThe temperature at destination" \
                     " address is {}°F,\n and at origin is {}°F".format(theDistance, theDuration, originWeather,
                                                                        destinationWeather)

        except (ValueError, IndexError, urllib.error.URLError, urllib.error.HTTPError):
            Factory.ErrorPop().open()

    def GoogleMap(self):
        originAddress = GoogleMapAPI.read_address(self.ids.Origin.text)
        destinationAddress = GoogleMapAPI.read_address(self.ids.Destination.text)
        try:
            GoogleMapAPI.get_map(originAddress, destinationAddress)
        except (ValueError, IndexError, urllib.error.URLError, urllib.error.HTTPError):
            Factory.ErrorPop().open()


class ScreenTwo(Screen):

    def recommended_hotels(self):
        start_time = int(self.ids.start_hour.text) * 60 + int(self.ids.start_min.text)
        lunch_time = int(self.ids.lunch_hour.text) * 60 + int(self.ids.lunch_min.text)
        sleep_time = int(self.ids.sleep_hour.text) * 60 + int(self.ids.sleep_min.text)
        daily_time = 14
        if start_time < lunch_time:
            first_day_time = lunch_time - start_time + sleep_time - lunch_time - 2
        else:
            first_day_time = sleep_time - start_time
        total_time = first_day_time
        while total_time < theDuration:
            address = hotel_restaurant_API.find_place(originAddress, desti)
            total_time += daily_time


    def nearby_restaurants(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Restaurants'


class ScreenHotels(Screen):
    pass


class ScreenRestaurants(Screen):
    def current_location(self) -> str:
        coordinates = GoogleMapAPI.get_location()
        print(coordinates['neighborhood'])
        return coordinates['neighborhood']

    def restaurants(self) -> str:
        current_loc = self.current_location()
        answer = ""
        for dist in range(5, 30):
            current_list = hotel_restaurant_API.find_restaurant(current_loc, 'food', 4.0, dist, 5)
            for one in current_list:
                answer = answer + one['Name'] + '\n' + one['Distance'] + ' miles, ' + one['Rating'] + ',\n' +\
                         one['Address'] + '\n' + one['Phone'] + '\n'
            if len(answer) > 0:
                break
        return answer

class ScreenManagement(ScreenManager):
    pass


Run = Builder.load_file("Screens.kv")


class MainApp(App):
    # def on_start(self):
    #     self.root_window.maximize()

    def build(self):
        return ScreenManagement()


MainApp().run()
