from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import json
from datetime import date

# 设置窗口大小（电脑调试用）
Window.size = (400, 700)

class HandBookLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 20

        # 标题
        self.title_label = Label(text="我的手帐本", font_size=30, size_hint_y=0.1)
        self.add_widget(self.title_label)

        # 日期显示
        self.today = str(date.today())
        self.date_label = Label(text=f"今日：{self.today}", font_size=18, size_hint_y=0.05)
        self.add_widget(self.date_label)

        # 输入框
        self.note_input = TextInput(
            hint_text="在这里写下你的手帐内容...",
            size_hint_y=0.6,
            font_size=16
        )
        self.add_widget(self.note_input)

        # 按钮区域
        btn_box = BoxLayout(size_hint_y=0.1, spacing=10)
        self.save_btn = Button(text="保存手帐", on_press=self.save_note)
        self.load_btn = Button(text="查看过往", on_press=self.load_notes)
        btn_box.add_widget(self.save_btn)
        btn_box.add_widget(self.load_btn)
        self.add_widget(btn_box)

    # 保存记录到json文件
    def save_note(self, instance):
        content = self.note_input.text.strip()
        if not content:
            return
        try:
            with open("handbook.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []
        data.append({"date": self.today, "content": content})
        with open("handbook.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.note_input.text = ""

    # 读取所有手帐
    def load_notes(self, instance):
        try:
            with open("handbook.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = [{"date":"暂无记录","content":"还没有写任何手帐"}]
        result_text = ""
        for item in data:
            result_text += f"【{item['date']}】\n{item['content']}\n\n"
        self.note_input.text = result_text

class HandBookApp(App):
    def build(self):
        return HandBookLayout()

if __name__ == "__main__":
    HandBookApp().run()