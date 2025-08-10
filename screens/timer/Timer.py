from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class TimerScreen(Screen):
    time_display = ObjectProperty(None)
    hours_input = ObjectProperty(None)
    minutes_input = ObjectProperty(None)
    seconds_input = ObjectProperty(None)
    
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
        try:
            hours = int(self.hours_input.text) if self.hours_input.text else 0
            minutes = int(self.minutes_input.text) if self.minutes_input.text else 0
            seconds = int(self.seconds_input.text) if self.seconds_input.text else 0
            
            controller = self.manager.timerController
            controller.start_timer(hours, minutes, seconds, self.timer_complete)
        except ValueError:
            pass  # Handle invalid input
    
    def stop(self):
        controller = self.manager.timerController
        controller.stop()
    
    def reset(self):
        controller = self.manager.timerController
        controller.reset()
        self.update_display(0)
        
    def timer_complete(self):
        # Could display a popup or play a sound
        pass