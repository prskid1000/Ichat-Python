from kivy.app import App
from kivy.config import Config
from kivy.core import window
from kivy.core.text import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, RoundedRectangle 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import requests
from requests.models import requote_uri

#Global variables acting as cookies
screenx = float(Config.get('graphics', 'width'))
screeny = float(Config.get('graphics', 'height'))

class Badge(Widget):

    def __init__(self, **kwargs): 
        super(Badge, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = (None, None)
        self.pos = (590, 10)
        self.size = (180, 30)
        with self.canvas.before:
            Color(1, 0.3, 0.3, 1)
            RoundedRectangle(pos=self.pos,size=self.size, 
            radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
            
    def on_touch_down(self, touch):
        with self.canvas:
            Color(0.3, 0.3, 0.3, 1)
            RoundedRectangle(pos=self.pos,size=self.size, 
            radius=[(10, 10), (10, 10), (10, 10), (10, 10)])

    def on_touch_up(self, touch):
        with self.canvas:
            Color(1, 0.3, 0.3, 1)
            RoundedRectangle(pos=self.pos,size=self.size, 
            radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
