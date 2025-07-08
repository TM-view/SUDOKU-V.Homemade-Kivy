from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class BackGround(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.7, 0.5, 0.5)
            self.rect = Rectangle(pos = self.pos, size = self.size)
        self.bind(pos = self.update_rect, size = self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
class Main(App):
    def build(self):
        return BackGround()

if __name__ == "__main__":
    Main().run()