from logging import disable
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.text import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#Global variables acting as cookies
screenx = float(Config.get('graphics', 'width'))
screeny = float(Config.get('graphics', 'height'))

userid = ["userid"]
listener = ["listener"]
password = ["password"]
boxids = ["boxids"]
comment = ["comment"]

#DOM Root
root = FloatLayout() 

#Components
def button(i, j, text, press):

    def function(event):
        press()

    button = Button()
    button.text = text
    button.pos = (i, j)
    button.size = (100, 30)
    button.background_color = (255, 1, 1, 1)
    button.bind(on_press = function) 
    return button

def send(press):

    def function(event):
        press()

    button = Button()
    button.text = "Send"
    button.font_size = "18sp"
    button.pos = (590, 200)
    button.size = (180, 40)
    button.background_color = (255, 1, 1, 1)
    button.bind(on_press = function) 
    return button

def label(i, j, text):
    label = Label()
    label.font_size = '18sp'
    label.pos = (i, j)
    label.text = text
    return label

def banner_and_background(Screen):
    with Screen.canvas:
        Color(0.4, 0.4, 0.4, 0.3)
        Rectangle(pos=root.pos, size=(screenx, screeny))
        Color(0.2, 0.2, 0.2, 0.7)
        Rectangle(pos=(150,500), size=(500, 100))
    label = Label()
    label.font_size = '36sp'
    label.pos = (350, 500)
    label.text = "IChat-Desktop"
    Screen.add_widget(label)

def subhead(Screen, text, i, j):
    label = Label()
    label.font_size = '30sp'
    label.pos = (i, j)
    label.text = text
    Screen.add_widget(label)


def textinput(i, j, var):
    textinput = TextInput()
    textinput.pos = (i, j)
    textinput.font_size = '16sp'
    textinput.size = (150, 30)

    def function(instance, value):
        var[0] = value

    textinput.bind(text = function)
    return textinput

def message(var):
    textinput = TextInput()
    textinput.pos = (590, 255)
    textinput.font_size = '16sp'
    textinput.size = (180, 140)

    def function(instance, value):
        var[0] = value

    textinput.bind(text = function)
    return textinput


def Send():
    req = {'userid': userid[0], 'boxid': listener[0], 'message': comment[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/sendbox",data=req).json()
    root.clear_widgets()
    root.add_widget(Chat())


def Delete():

    req = {'userid':userid[0], 'boxid': listener[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/unsetbox",data=req).json()
    
    req = {'boxid': listener[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/deletebox",data=req).json()

    req = {'userid':listener[0][listener[0].index('-') + 1:], 'boxid': listener[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/unsetbox",data=req).json()
    Login()


def Mail(author, message):

    mail = BoxLayout(orientation='horizontal')
    mail.size_hint = (1, None)

    label = Button(disabled=True)
    mess = Button(disabled=True)

    label.text =  author
    mess.text =  message

    mess.color = (0,0,0, 1)
    mess.background_color = (255,255,255, 255)

    mess.size_hint = (6, 1)
    label.size_hint = (1, 1)

    if(author == userid[0]):
        label.background_color = (1,1,255, 1)
    else:
        label.background_color = (255,1,1, 1)  


    if(author == userid[0]):
        mail.add_widget(label)
        mail.add_widget(mess)
    else:
        mail.add_widget(mess)
        mail.add_widget(label)


    return mail

def scrollgridChat(Screen,components,pos, size):
    grid = GridLayout(cols=1, size_hint_y=None)
    grid.bind(minimum_height=grid.setter('height'))
    for i in components:
        grid.add_widget(Mail(i['author'], i['message']))

    scroll = ScrollView(size_hint=(1, None), pos=pos, size=size)
    scroll.do_scroll_y = True
    scroll.do_scroll_x = False
    scroll.add_widget(grid)
    return scroll


def Refresh(dt):
    root.clear_widgets()
    root.add_widget(Chat())

def Reload(dt):
    root.clear_widgets()
    root.add_widget(Index())


def Chat():
    Chat = Widget()
    banner_and_background(Chat)

    req = {'boxid': listener[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/getbox",data=req).json()

    with Chat.canvas:
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(40,50), size=(500, 400))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(60,50), size=(480, 400))

        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(580,250), size=(200, 200))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(590, 255), size=(180, 140))

    subhead(Chat,"Message", 630, 375)
    subhead(Chat, listener[0], 250, 375)

    Chat.add_widget(message(comment))
    Chat.add_widget((send(Send)))

    Chat.add_widget(button(570, 130, "Delete", Delete))
    Chat.add_widget(button(680, 130, "GO Back", Login))

    if(type(res['data']) != str):
        res['data']['chat'].reverse()
        Chat.add_widget(scrollgridChat(Chat, res['data']['chat'], pos=(60,60), size=(480, 340)))

    Clock.schedule_once(Refresh, 10)

    return Chat

def scrollgrid(Screen,components,pos, size):
    grid = GridLayout(cols=1, size_hint_y=None)
    grid.bind(minimum_height=grid.setter('height'))
    for i in components:
        grid.add_widget(i)

    scroll = ScrollView(size_hint=(1, None), pos=pos, size=size)
    scroll.do_scroll_y = True
    scroll.do_scroll_x = False
    scroll.add_widget(grid)
    return scroll

def Badge(text, press, **kwargs):

    def function(event):
        press(kwargs)

    button = Button()
    button.size_hint = (None, None)
    button.text = text
    button.size = (180, 30)
    button.background_color = (255, 1, 1, 1)
    button.bind(on_press = function) 
    return button

def Card(text):

    def function(event):
        listener[0] = text
        Clock.unschedule(Reload)
        root.clear_widgets()
        root.add_widget(Chat())

    card = Button()
    card.size_hint = (None, None)
    card.text = text
    card.font_size = "24sp"
    card.size = (480, 100)
    card.background_color = (255, 1, 1, 1)
    card.bind(on_press = function) 
    return card

def New(data):

    boxid = "#" + userid[0] + "-" + data['data']
    req = {'userid':userid[0], 'boxid': boxid, 'message': 'Hi, ' + data['data']}
    res = requests.post(url = "https://ichatb.herokuapp.com/sendbox",data=req).json()

    req = {'userid':userid[0], 'boxid': boxid}
    res = requests.post(url = "https://ichatb.herokuapp.com/setbox",data=req).json()

    req = {'userid':data['data'], 'boxid': boxid}
    res = requests.post(url = "https://ichatb.herokuapp.com/setbox",data=req).json()

    listener[0] = boxid

    Clock.unschedule(Reload)
    root.clear_widgets()
    root.add_widget(Chat())

def Index():
    Index = Widget()
    banner_and_background(Index)
    with Index.canvas:
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(40,50), size=(500, 400))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(60,50), size=(480, 400))
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(580,50), size=(200, 400))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(590,60), size=(180, 340))
    subhead(Index,"Users", 630, 375)
    subhead(Index,"Your Boxes", 250, 375)

    res = requests.get(url = "https://ichatb.herokuapp.com/getusers").json()

    set = []

    for i in res['data']:
        if(i['userid'] != userid[0]):
            set.append(Badge(i['userid'], New, data=i['userid']))
    
    Index.add_widget(scrollgrid(Index, set, pos=(590,60), size=(180, 340)))

    set = []

    for i in boxids[0]:
        set.append(Card(text=str(i)))
    
    Index.add_widget(scrollgrid(Index, set, pos=(60, 60), size=(480, 340)))
    
    Clock.schedule_once(Reload, 20)

    return Index

def Login():
    data = {'userid':userid[0], 'password': password[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/isauth",data=data).json()
    if(res['success'] == "True"):
        boxids[0] = res['data']['boxid']
        root.clear_widgets()
        root.add_widget(Index())
    else:
        root.clear_widgets()
        root.add_widget(Account())
    Clock.unschedule(Refresh)

def Register():
    data = {'userid':userid[0], 'password': password[0]}
    res = requests.post(url = "https://ichatb.herokuapp.com/adduser",data=data).json()
    if(res['success'] == "True"):
        boxids[0] = res['data']['boxid']
    if(res['success'] == "True"):
        boxids[0] = res['data']['boxid']
        root.clear_widgets()
        root.add_widget(Index())
    else:
        root.clear_widgets()
        root.add_widget(Account())
    Clock.unschedule(Refresh)
    
def Account():
    Account = Widget()
    banner_and_background(Account)
    with Account.canvas:
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(60,150), size=(250, 320))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(150,150), size=(160, 320))
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(415,150), size=(250, 320))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(505,150), size=(160, 320))
    Account.add_widget(label(50, 400, "Userid"))
    Account.add_widget(label(65, 320, "Password"))
    Account.add_widget(label(405, 400, "Userid"))
    Account.add_widget(label(420, 320, "Password"))
    Account.add_widget(label(455, 240, "Re-Enter Password"))
    Account.add_widget(textinput(440, 235, password))
    Account.add_widget(textinput(80, 400, userid))
    Account.add_widget(textinput(80, 320, password))
    Account.add_widget(textinput(440, 400, userid))
    Account.add_widget(textinput(440, 320, password))
    Account.add_widget(button(180, 250, "Login", Login))
    Account.add_widget(button(550, 165, "Register", Register))
    return Account

root.add_widget(Account())

class App(App):
    def build(self):
        return root

if __name__ == "__main__":
    App().run()
