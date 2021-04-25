import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.clock import Clock


class ScreenLoading(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.go_to_main, 3)

    def go_to_main(self, dt):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Start'


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    pass


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
