import kivy
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.clock import Clock


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
    # Requires database
    pass


class ScreenOne(Screen):
    def go_forward(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Implement'

    def getUsername(self) -> str:
        return 'aa'


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

    def build(self):
        return ScreenManagement()


MainApp().run()
