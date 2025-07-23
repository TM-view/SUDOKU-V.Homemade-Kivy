from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
import random

class Selcet_Num(Button):
    instances = []
    lastes = 0
    button_refs = {}
    
    def __init__(self, number, label=None, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1,1,1,0)
        self.color = (0,0,0,1)
        self.number = number
        self.label = label
        Selcet_Num.instances.append(self)
        Selcet_Num.button_refs[number] = self
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
        self.bind(size=self.relayout_numbers, pos=self.relayout_numbers)  # ✅ เพิ่ม bind ตรงนี้
        self.highlighted_number = None
        self.min_random = 2
        self.max_random = 5
        self.miss = [0 for _ in range(9)]
        self.lines = []
        self.wrong_count = 0
        self.warning_label = None
        self.cell_labels = {}
        self.answer_values = {}  # ✅ เก็บค่าที่สุ่มไว้
        self.player_values = {}

        with self.canvas:
            Color(1, 1, 1, 1)
            for j in range(10):
                w = 3 if j % 3 == 0 else 1
                self.lines.append(Line(points=[], width=w))
            for k in range(10):  # ✅ 9 แถวต้องมีแค่ 10 เส้นแนวนอน
                w = 3 if k % 3 == 0 else 1
                self.lines.append(Line(points=[], width=w))

    def fill_random_numbers(self):
        self.cell_labels.clear()
        self.clear_widgets()
        self.answer_values.clear()

        # ✅ ใช้ตาราง list 2 มิติเพื่อเก็บตัวเลข
        self.grid_values = [[0 for _ in range(9)] for _ in range(9)]

        # ✅ สร้าง Sudoku โดยใช้ backtracking
        def is_safe(row, col, num):
            # ตรวจแถว
            if num in self.grid_values[row]:
                return False
            # ตรวจคอลัมน์
            for r in range(9):
                if self.grid_values[r][col] == num:
                    return False
            # ตรวจในบล็อค 3x3
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    if self.grid_values[r][c] == num:
                        return False
            return True

        def solve_cell(row, col):
            if row == 9:
                return True  # จบแล้ว

            next_row, next_col = (row + 1, 0) if col == 8 else (row, col + 1)

            nums = list(range(1, 10))
            random.shuffle(nums)  # ✅ สุ่มลำดับการลองเลข

            for num in nums:
                if is_safe(row, col, num):
                    self.grid_values[row][col] = num
                    if solve_cell(next_row, next_col):
                        return True
                    self.grid_values[row][col] = 0  # backtrack

            return False

        # ✅ เริ่มสร้าง Sudoku
        solve_cell(0, 0)

        def miss_table(row, col):
            value = 0
            if row <= 2:
                if col <= 2:
                    value = 0
                elif col > 2 and col <= 5:
                    value = 1
                else :
                    value = 2
            elif row > 2 and row <= 5:
                if col <= 2:
                    value = 3
                elif col > 2 and col <= 5:
                    value = 4
                else :
                    value = 5
            else :
                if col <= 2:
                    value = 6
                elif col > 2 and col <= 5:
                    value = 7
                else :
                    value = 8
                    
            self.miss[value] += 1
            if self.miss[value] < self.min_random or self.miss[value] > self.max_random :
                return False
            else :
                return True
            
        # ✅ ย้ายค่าไปไว้ใน answer_values
        for row in range(9):
            for col in range(9):
                rd = random.randint(0,2)
                if rd < 2 and not miss_table(row,col):
                    pass
                else :
                    self.player_values[(row, col)] = self.grid_values[row][col]
                    
                self.answer_values[(row, col)] = self.grid_values[row][col]
                    
        # ✅ แสดงเลข
        self.relayout_numbers()
        self.update_select_buttons()

    def relayout_numbers(self, *args):
        # ล้างของเก่า
        for label in self.cell_labels.values():
            self.remove_widget(label)
        self.cell_labels.clear()

        cell_width = self.width / 9
        cell_height = self.height / 9

        for (row, col), value in self.player_values.items():
            center_x = self.x + col * cell_width + cell_width / 2
            center_y = self.y + (8 - row) * cell_height + cell_height / 2

            color = (0, 0, 0, 1) if value == self.answer_values[(row, col)] else (1, 0, 0, 1)

            num_label = Label(
                text=str(value),
                font_size='30sp',
                size_hint=(None, None),
                size=(cell_width, cell_height),
                halign='center',
                valign='middle',
                color=color
            )
            num_label.bind(size=num_label.setter('text_size'))
            num_label.center = (center_x, center_y)

            self.add_widget(num_label)
            self.cell_labels[(row, col)] = num_label

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            x, y = touch.pos

            cell_width = self.width / 9
            cell_height = self.height / 9

            row = int((self.top - y) / cell_height)
            col = int((x - self.x) / cell_width)

            if not (0 <= row <= 8 and 0 <= col <= 8):
                return True

            from __main__ import Selcet_Num

            if Selcet_Num.lastes == 0:
                print("ยังไม่ได้เลือกเลข")
                return True

            # ตรวจสอบว่าตำแหน่งนี้ล็อคไว้หรือไม่
            correct_value = self.answer_values.get((row, col))
            current_value = self.player_values.get((row, col))

            # ถ้าเลขถูกต้องแล้ว ไม่อนุญาตให้เปลี่ยน
            if current_value == correct_value:
                return True

            # อัปเดตเลขใน player_values
            self.player_values[(row, col)] = Selcet_Num.lastes

            # แก้ไขหรือเพิ่ม label
            if (row, col) in self.cell_labels:
                label = self.cell_labels[(row, col)]
                label.text = str(Selcet_Num.lastes)
            else:
                pos_x = self.x + col * cell_width
                pos_y = self.y + (8 - row) * cell_height

                label = Label(
                    text=str(Selcet_Num.lastes),
                    font_size='30sp',
                    size_hint=(None, None),
                    size=(cell_width, cell_height),
                    pos=(pos_x, pos_y),
                    halign='center',
                    valign='middle',
                    color=(0, 0, 0, 1)
                )
                label.bind(size=label.setter('text_size'))
                self.add_widget(label)
                self.cell_labels[(row, col)] = label

            # เปลี่ยนสีเลขตามความถูกต้อง
            if self.player_values[(row, col)] == self.answer_values[(row, col)]:
                label.color = (0, 0, 0, 1)  # ถูก = สีดำ
            else:
                label.color = (1, 0, 0, 1)  # ผิด = สีแดง
                self.wrong_count += 1
                self.show_warning(f"You Wrong ({self.wrong_count}/3)")
                if self.wrong_count >= 3:
                    self.game_over()

            self.update_select_buttons()
            return True

        return super().on_touch_down(touch)
    
    def show_warning(self, message):
        if self.warning_label:  # ถ้ามีป้ายเตือนเก่า ลบก่อน
            self.remove_widget(self.warning_label)

        self.warning_label = Label(
            text=message,
            font_size='36sp',
            color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos=(self.center_x - 150, self.center_y),
            halign='center',
            valign='middle'
        )
        self.warning_label.bind(size=self.warning_label.setter('text_size'))
        self.add_widget(self.warning_label)

        def remove_warning(dt):
            if self.warning_label:
                self.remove_widget(self.warning_label)
                self.warning_label = None

        Clock.schedule_once(remove_warning, 2)  # หายภายใน 2 วินาที


    def update_grid(self, *args):
        width = self.width
        height = self.height
        for i in range(10):
            x = self.x + (width / 9) * i
            self.lines[i].points = [x, self.y, x, self.y + height]
        for i in range(10):
            y = self.y + (height / 9) * i
            self.lines[i + 10].points = [self.x, y, self.x + width, y]
    
    def toggle_highlight_number(self, number):
        # สลับเลขที่กำลังไฮไลต์
        if self.highlighted_number == number:
            self.highlighted_number = None
        else:
            self.highlighted_number = number

        # อัปเดตสีทั้งหมด
        for (row, col), label in self.cell_labels.items():
            val = self.player_values.get((row, col), 0)
            correct = self.answer_values.get((row, col), 0)

            # ถ้าตอบถูก → อนุญาตให้ไฮไลต์
            if val == correct and val == number:
                label.color = (0, 1, 0, 1) if self.highlighted_number == number else (0, 0, 0, 1)
            else:
                # ถ้าเป็นช่องที่กรอกผิด → แดง
                if val != 0 and val != correct:
                    label.color = (1, 0, 0, 1)
                else:
                    label.color = (0, 0, 0, 1)
                    
    def update_select_buttons(self):
        from __main__ import Selcet_Num
        # นับจำนวนของแต่ละเลขใน player_values
        count = {i: 0 for i in range(1, 10)}
        for (row, col), value in self.player_values.items():
            if value == self.answer_values.get((row, col), 0):
                count[value] += 1

        for i in range(1, 10):
            btn = Selcet_Num.button_refs.get(i)
            lbl = btn.label if btn else None
            if count[i] >= 9:
                if Selcet_Num.lastes == i :
                    Selcet_Num.lastes = 0
                btn.disabled = True
                btn.text = ""  # ✅ ซ่อนปุ่ม
                if lbl:
                    lbl.text = ""
            else:
                btn.disabled = False
                if lbl:
                    lbl.text = str(i)
                    
    def game_over(self):
        self.warning_label = None  # ล้างป้ายเตือนหากยังอยู่

        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        message = Label(text="Game Over!\nYou missed 3 times.", font_size='24sp', halign='center')

        btn_retry = Button(text="Play Again", size_hint=(1, 0.3), font_size='20sp')
        popup_layout.add_widget(message)
        popup_layout.add_widget(btn_retry)

        popup = Popup(title="Game Over", content=popup_layout,
                    size_hint=(0.6, 0.4), auto_dismiss=False)
        
        def restart_game(instance):
            popup.dismiss()
            
            # ✅ เคลียร์ค่าต่าง ๆ
            self.wrong_count = 0
            self.miss = [0 for _ in range(9)]
            self.player_values.clear()
            self.cell_labels.clear()
            self.clear_widgets()

            # ✅ ล้างเลขที่เลือก
            from __main__ import Selcet_Num
            Selcet_Num.lastes = 0
            for btn in Selcet_Num.instances:
                btn.color = (0, 0, 0, 1)
                if btn.label:
                    btn.label.color = (0, 0, 0, 1)
                    btn.label.text = str(btn.number)
                btn.disabled = False

            self.fill_random_numbers()

        btn_retry.bind(on_press=restart_game)
        popup.open()
            
class BackGround(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 0.7, 0.5, 0.5)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # สร้าง layout หลัก: แนวตั้ง แบ่งพื้นที่
        main_layout = BoxLayout(orientation='vertical')
        self.add_widget(main_layout)

        # พื้นที่ปุ่มเลือกตัวเลข (10% ด้านบน)
        button_bar = FloatLayout(size_hint=(1, 0.1))
        for num in range(1, 10):
            label = Label(
                text=str(num),
                pos_hint={'x': (num - 1) / 9, 'y': 0},
                size_hint=(1 / 9, 1),
                font_size='30sp',
                color=(0, 0, 0, 1),
                font_name='Roboto-Bold.ttf'
            )
            sn = Selcet_Num(num, label,
                            size_hint=(1 / 9, 1),
                            pos_hint={'x': (num - 1) / 9, 'y': 0})
            button_bar.add_widget(sn)
            button_bar.add_widget(label)
        main_layout.add_widget(button_bar)

        # พื้นที่ตาราง (90% ด้านล่าง)
        self.grid = LineBlock(size_hint=(1, 0.9))
        main_layout.add_widget(self.grid)

        # สุ่มเลขหลัง layout เสร็จ
        Clock.schedule_once(self.populate_random_numbers_after_layout, 0)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def populate_random_numbers_after_layout(self, dt):
        self.grid.fill_random_numbers()
        
class Main(App):
    def build(self):
        return BackGround()

if __name__ == "__main__":
    Main().run()