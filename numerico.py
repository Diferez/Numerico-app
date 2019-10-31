import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import OptionProperty
class newton(Screen):
    def something(self):
        return(cholesky)
    pass
class biseccion(Screen):
    pass

class cholesky(Screen):
    pass

class menu(Screen):
    pass

def manager(screen_manager):
    screen_manager.add_widget(menu(name="menu"))
    screen_manager.add_widget(biseccion(name="biseccion"))
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