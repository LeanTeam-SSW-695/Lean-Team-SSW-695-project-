import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.clock import Clock
import mysql.connector
from mysql.connector.constants import ClientFlag


def set_connection():
    config = {
        'user': 'root',
        'host': '35.220.246.119',
        'password': "12345678",
        'client_flags': [ClientFlag.SSL]
    }
    return config


username = ""


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
        # Database required
        self.go_forward()


class ScreenRegister(Screen):
    def register(self):
        self.reg(self.username, self.password)
    def reg(username, pwd):
        config = set_connection()
        config['database'] = 'login'  # add new database to config dict
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()  # initialize connection cursor
        if login(username, pwd):
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


class ScreenOne(Screen):
    def go_forward(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Implement'


class ScreenTwo(Screen):
    def recommend(self):
        self.go_forward()

    def go_forward(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Plans'


class ScreenPlans(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


Run = Builder.load_file("Screens.kv")


class MainApp(App):
    # def on_start(self):
    #     self.root_window.maximize()

    def greetings_username(self) -> str:
        return 'Hello, ' + username

    def build(self):
        return ScreenManagement()


MainApp().run()
