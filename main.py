from kivy.app import App
from kivy.uix.label import Label

class Main(App):
    def build(self):
        return Label(text = 'Let\'Start It!')

if __name__ == "__main__":
    Main().run()