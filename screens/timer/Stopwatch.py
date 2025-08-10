from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class StopwatchScreen(Screen):
    time_display = ObjectProperty(None)
    
    def on_enter(self):
        self.update_event = Clock.schedule_interval(self.update_display, 0.1)
    
    def on_leave(self):
        if self.update_event:
            self.update_event.cancel()
    
    def update_display(self, dt):
        controller = self.manager.timerController
        if self.time_display:
            self.time_display.text = controller.get_time_string()
    
    def start(self):
        controller = self.manager.timerController
        controller.start_stopwatch()
    
    def stop(self):
        controller = self.manager.timerController
        controller.stop()
    
    def reset(self):
        controller = self.manager.timerController
        controller.reset()
        self.update_display(0)