from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
import json ,glob
from datetime import datetime
import random
from pathlib import Path

Builder.load_file("design.kv")



class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current ="signup_screen"
    def login(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password']==pword:
            self.manager.current="log_in_screen_success"
        else:
            self.ids.wrong_input.text="invalid username or password"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname , pword):
        with open("users.json") as file:
            users = json.load(file)
        users[uname]={"username":uname,"password":pword,"created":datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json",'w') as file:
            json.dump(users,file)

        self.manager.current= "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def log_in_page(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LogInScreenSuccess(Screen):
    def log_out(self):
        self.manager.current = "login_screen"

    def get_quote(self,feel):
        feel =feel.lower()
        available_feeling =glob.glob("quotes/*txt")
        available_feeling =[Path(filename).stem  for filename in available_feeling]

        if feel in available_feeling:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text=random.choice(quotes)

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()