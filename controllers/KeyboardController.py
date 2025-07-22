from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class KeyboardController:
    def __init__(self, app):
        self.app = app
        self.root = None  # This will be set to the root of the app later
        self.current_input = None  # Track the currently focused TextInput
        self.shift_active = False
        self.capslock_active = False


    def on_key_press(self, keyboard, keycode, *args):
        print(f"KEY PRESSED: {keycode}")
        if not self.current_input:
            return

        key = keycode[1]

        if key == 'backspace':
            self.current_input.text = self.current_input.text[:-1]
        elif key == 'enter':
            self.HideKeyboard()
        elif key == 'spacebar':
            self.current_input.text += ' '
        elif key == 'shift':
            self.shift_active = not self.shift_active
        elif key == 'capslock':
            self.capslock_active = not self.capslock_active
        elif len(key) == 1:
            # Decide casing
            if self.shift_active ^ self.capslock_active:
                key = key.upper()
            else:
                key = key.lower()
            self.current_input.text += key

            # If shift was active (but not caps), reset it after 1 key
            if self.shift_active and not self.capslock_active:
                self.shift_active = False

class TouchInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = None

    def on_focus(self, instance, value):
        if value:
            # Always release any existing keyboard first
            if self.keyboard:
                self.keyboard.unbind(on_key_down=self._on_key_down)
                self.keyboard.release()
                self.keyboard = None

                # Request new keyboard
                self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
                if self.keyboard:
                    self.keyboard.bind(on_key_down=self._on_key_down)

            else:
                if self.keyboard:
                    self.keyboard.unbind(on_key_down=self._on_key_down)
                    self.keyboard.release()
                    self.keyboard = None

    def _keyboard_closed(self):
        self.focus = False
        self.keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key == 'backspace':
            if self.selection_text:
                self.delete_selection()
            else:
                self.text = self.text[:-1]  # fallback
        elif key == 'enter':
            if self.multiline:
                self.insert_text('\n')
                return True

            # Move to next input if available
            parent = self.parent
            inputs = [w for w in parent.walk() if isinstance(w, TouchInput)]
            inputs.sort(key=lambda w: w.y, reverse=True)  # top to bottom

            try:
                i = inputs.index(self)
                next_input = inputs[i + 1]
                next_input.focus = True
            except (ValueError, IndexError):
                self.focus = False  # blur if no more inputs
        elif len(key) == 1:
            self.insert_text(key)
        return True
