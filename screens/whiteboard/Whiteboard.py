from kivy.uix.screenmanager import Screen
from screens.widgets.Canvas import CanvasWidget  # Import the drawing widget
from kivy.factory import Factory
Factory.register('CanvasWidget', cls=CanvasWidget)

class WhiteboardScreen(Screen):
    pass
    