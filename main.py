from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget

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
                
            for k in range(10):  # 10 เส้นแนวนอน
                if k % 3 == 0 : w = 3 
                else : w = 1
                self.lines.append(Line(points=[], width = w))

    def update_grid(self, *args):
        width = self.width
        height = self.height

        # คำนวณตำแหน่งเส้นแนวตั้ง (x คงที่)
        for i in range(10):
            x = self.x + (width / 9) * i
            self.lines[i].points = [x, self.y, x, self.y + height]

        # คำนวณตำแหน่งเส้นแนวนอน (y คงที่)
        for i in range(10):
            y = self.y + (height / 9) * i
            self.lines[i + 10].points = [self.x, y, self.x + width, y]
            
class BackGround(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.7, 0.5, 0.5)
            self.rect = Rectangle(pos = self.pos, size = self.size)
        self.bind(pos = self.update_rect, size = self.update_rect)
        self.add_widget(LineBlock())
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
class Main(App):
    def build(self):
        return BackGround()

if __name__ == "__main__":
    Main().run()