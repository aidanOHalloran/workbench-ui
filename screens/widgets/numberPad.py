from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file("kv/numberPad/numberPad.kv")

class NumberPad(BoxLayout):
    text = StringProperty("")  # Matches `TextInput.text` API

    def insert_char(self, char):
        self.text += char

    def backspace(self):
        self.text = self.text[:-1]

    def clear(self):
        self.text = ""

    def done(self):
        # Optional: emit event, do nothing, or trigger parent handler
        print(f"Final value: {self.text}")
