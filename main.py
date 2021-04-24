from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


Builder.load_file("Screens.kv")


class PageOne(Screen):
    pass


class PageTwo(Screen):
    pass


class PagePlans(Screen):
    pass


class RunApp(App):
    def build(self):
        screens = ScreenManager()
        screens.add_widget(PageOne(name="Welcome to Travel Companion"))
        screens.add_widget(PageTwo(name="Implement Your Schedule"))
        screens.add_widget(PagePlans(name="Here Are Recommended Plans"))
        return screens


RunApp().run()
