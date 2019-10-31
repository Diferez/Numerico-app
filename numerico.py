import kivy

from kivy.app import App
from kivy.properties import OptionProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

from kivy.clock import Clock
import time


from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import libs

class newton(Screen):
    pass
class biseccion(Screen):
    data_items = ListProperty([1,2,3])
    def popu(self):
        self.add_widget(Label(text='pass'))
        
class runBiseccion(Screen):
    def __init__(self, **kwargs):
        super(runBiseccion, self).__init__(**kwargs)

    def start(self):
        Xi=float(self.manager.get_screen("biseccion").ids.Xi.text)
        Xs=float(self.manager.get_screen("biseccion").ids.Xs.text)
        Tol =float(self.manager.get_screen("biseccion").ids.Tol.text)
        Ite = int(self.manager.get_screen("biseccion").ids.Ite.text)
        F = parse_expr(self.manager.get_screen("biseccion").ids.F.text.replace('^','**'))
        x = Symbol('x')
        F = lambdify(x, F)
        print(Xi,Xs,Tol,Ite,F)
        r,lista = libs.biseccion(F,Xi,Xs,Ite,Tol)
        self.data = [{'text': str(x)} for x in lista]
    

        

        

class cholesky(Screen):
    pass

class menu(Screen):
    pass

def manager(screen_manager):
    screen_manager.add_widget(menu(name="menu"))
    screen_manager.add_widget(biseccion(name="biseccion"))
    screen_manager.add_widget(runBiseccion(name="runBiseccion"))
    screen_manager.add_widget(newton(name="newton"))
    screen_manager.add_widget(cholesky(name="cholesky"))
    

class numericoApp(App):
    
    title = "Numerico"
    
    def build(self):
        screen_manager = ScreenManager()
        manager(screen_manager)

        return screen_manager
if __name__ == "__main__":
    numericoApp().run()