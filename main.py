import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
import mysql.connector
from mysql.connector.constants import ClientFlag
import GoogleMapAPI
import hotel_restaurant_API
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
    def go_Implement(self):
        global originAddress, destinationAddress
        originAddress = self.ids.Origin.text
        destinationAddress = self.ids.Destination.text
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Implement'

    def go_One(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Start'

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

        except:
            Factory.ErrorPop().open()
            return None
        originCoor = GoogleMapAPI.read_address(originAddress)
        destinCoor = GoogleMapAPI.read_address(destinationAddress)
        try:
            GoogleMapAPI.get_map(originCoor, destinCoor)
        except (ValueError, IndexError, urllib.error.URLError, urllib.error.HTTPError):
            Factory.ErrorPop().open()
            return None

        # Create Screen Information
        ScreenInformation = Screen(name='Information')
        layout = BoxLayout(orientation='vertical')
        ScreenInformation.add_widget(layout)
        layout.add_widget(Label(text='Trip Details', font_size=30, size_hint_y=.2))
        layout.add_widget(Image(source='GoogleMapsImage.png', size_hint_y=.5))
        layout.add_widget(Label(text=output, text_size=(self.width, None), size_hint_y=.25))
        layout.add_widget(Button(text='Back', on_release=self.go_One, size_hint_y=.2))
        self.manager.add_widget(ScreenInformation)

        # Goto Screen Information
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Information'


class ScreenImplement(Screen):
    def return_here(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Implement'

    def time_convert(self, mins):
        if mins >= 24 * 60:
            day = mins // (24 * 60)
            hour = mins % (24 * 60)
            if day > 1:
                return "%d days %d hours" % (day, hour)
            else:
                return '1 day %d hours' % hour
        else:
            hour = mins // 60
            min = mins % 60
            return "%d hours %d minutes" % (hour, min)

    def recommended_hotels(self):
        try:
            start_time = int(self.ids.start_hour.text) * 60 + int(self.ids.start_min.text)
            lunch_time = int(self.ids.lunch_hour.text) * 60 + int(self.ids.lunch_min.text)
            sleep_time = int(self.ids.sleep_hour.text) * 60 + int(self.ids.sleep_min.text)
        except:
            Factory.ErrorPop().open()
            return None
        daily_time = 14 * 60
        if start_time < lunch_time:
            first_day_time = abs(sleep_time - start_time) - 120
        else:
            first_day_time = abs(sleep_time - start_time)
        total_time = first_day_time
        day: int = 1
        Hotels = []

        originCoor = GoogleMapAPI.read_address(originAddress)
        destinCoor = GoogleMapAPI.read_address(destinationAddress)
        theDistance, theDuration = GoogleMapAPI.distance(originCoor, destinCoor)

        if len(theDuration.split()) == 4:
            if theDuration.split()[1] == 'hour' or theDuration.split()[1] == 'hours':
                duration = int(theDuration.split()[0]) * 60 + int(theDuration.split()[2])
            else:
                duration = int(theDuration.split()[0]) * 24 * 60 + int(theDuration.split()[2]) * 60
        else:
            duration = int(theDuration.split()[0])
        address = originAddress
        while total_time < duration:
            address = hotel_restaurant_API.find_place(address, destinationAddress, daily_time)
            print(address)
            if address is None:
                total_time += daily_time
                day += 1
                continue
            answer = "Day %d\n" % day
            current_list = hotel_restaurant_API.find_hotel(address, 60, 1)
            for one in current_list:
                answer = answer + one['Name'] + ', Rating: ' + str(one['Rating']) + ',\n' + \
                         one['Address'] + '\nOpen Now: ' + str(one['Open']) + '\n'
            if answer == "Day %d\n" % day:
                answer = answer + 'We cannot find the hotel for you to rest at night on Day %d\n' % day
            Hotels.append(answer)
            total_time += daily_time
            day += 1


        # Construct the Screen Hotels
        ScreenHotels = Screen(name='Hotels')
        layout = BoxLayout(orientation='vertical')
        ScreenHotels.add_widget(layout)
        layout.add_widget(Label(text='Recommended Hotels', font_size=30, size_hint_y=.2))
        if len(Hotels) == 0:
            layout.add_widget(
                Label(text='Your trip would end in one day, so no hotels would be planned for you', size_hint_y=.2))
        else:
            for hotel in Hotels:
                layout.add_widget(Label(text=hotel, size_hint_y=.2))
        layout.add_widget(Button(text='Back', on_release=self.return_here, size_hint_y=.15))
        self.manager.add_widget(ScreenHotels)
        # Switch to Screen Hotels
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Hotels'

    def nearby_restaurants(self):
        # Construct the Screen Restaurants
        ScreenRestaurants = Screen(name='Restaurants')
        layout = BoxLayout(orientation='vertical')
        ScreenRestaurants.add_widget(layout)
        layout.add_widget(Label(text='Nearby Restaurants', font_size=30))
        try:
            current_loc = self.current_location()
            #current_loc = originAddress
            layout.add_widget(Label(text='Your Current Location: ' + current_loc))
            layout.add_widget(Label(text=self.restaurants(current_loc), text_size=self.size))
        except:
            Factory.ErrorPop().open()
            return None
        layout.add_widget(Button(text='Back', on_release=self.return_here, size_hint_y=.15))
        self.manager.add_widget(ScreenRestaurants)

        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Restaurants'

    def current_location(self) -> str:
        coordinates = GoogleMapAPI.get_location()
        return coordinates['neighborhood']

    def restaurants(self, current_loc) -> str:
        answer = ""
        current_list = hotel_restaurant_API.find_restaurant(current_loc, 'food', 3.0, 60, 5)
        for one in current_list:
            answer = answer + one['Name'] + '\n' + one['Distance'] + ' miles, Rating: ' + str(one['Rating']) + ',\n' + \
                     one['Address'] + '\n' + one['Phone'] + '\n\n'
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
