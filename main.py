from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

class Selcet_Num(Button):
    instances = []
    lastes = 0
    
    def __init__(self, number, label=None, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1,1,1,0)
        self.color = (0,0,0,1)
        self.number = number
        self.label = label
        Selcet_Num.instances.append(self)
        self.bind(on_press = self.on_button_press)
        
    def on_button_press(self, instance) :
        Selcet_Num.lastes = self.number
        for obj in Selcet_Num.instances:
            if obj.number == self.number : 
                obj.color = (0,0,1,1) 
                obj.label.color = (0,0,1,1)
            else :
                obj.color = (0,0,0,1)
                obj.label.color = (0,0,0,1)
        
class LineBlock(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_grid, pos=self.update_grid)
        self.lines = []

        with self.canvas:
            Color(1, 1, 1, 1)  # สีขาว
            # สร้างเส้นไว้ก่อน (6 เส้น: 3 แนวตั้ง, 3 แนวนอน)
            for j in range(10):  # 10 เส้นแนวตั้ง
                if j % 3 == 0 : w = 3
                else : w = 1
                self.lines.append(Line(points=[], width = w))
                
            for k in range(11):  # 10 เส้นแนวนอน
                if k % 3 == 0 : w = 3 
                else : w = 1
                self.lines.append(Line(points=[], width = w))

    def update_grid(self, *args):
        width = self.width
        height = self.height

        # คำนวณตำแหน่งเส้นแนวตั้ง (x คงที่)
        for i in range(10):
            x = self.x + (width / 9) * i
            self.lines[i].points = [x, self.y, x, self.y + height - (height / 9.6)]

        # คำนวณตำแหน่งเส้นแนวนอน (y คงที่)
        for i in range(11):
            y = self.y + (height / 10) * i
            self.lines[i + 10].points = [self.x, y, self.x + width, y]
            
class BackGround(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.7, 0.5, 0.5)
            self.rect = Rectangle(pos = self.pos, size = self.size)
        self.bind(pos = self.update_rect, size = self.update_rect)
        self.add_widget(LineBlock())
        # Window.size = (720,1280) # แนวตั้ง
        # Window.size = (1280,720) # แนวนอน
        for num in range(1,10) :
            label = Label(text=str(num), pos_hint={'x':(num-1) / 9, 'y': 0.9}, size_hint=(1/9, 0.1), 
                  font_size='30sp', color=(0,0,0,1), font_name='Roboto-Bold.ttf')
            sn = Selcet_Num(num, label, size_hint = (1/5, 1), pos_hint = {'x': (num-1) / 9, 'y': 0.9})
            self.add_widget(sn)
            self.add_widget(label)   
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
class Main(App):
    def build(self):
        return BackGround()

if __name__ == "__main__":
    Main().run()