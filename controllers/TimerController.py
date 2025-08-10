from kivy.clock import Clock
from kivy.properties import NumericProperty

class TimerController:
    def __init__(self, app):
        self.app = app
        self.root = None  # This will be set to the root of the app later
        self.running = False
        self.time = 0  # For stopwatch: elapsed time, For timer: remaining time
        self.timer_event = None
        self.mode = None  # 'timer' or 'stopwatch'
        self.callback = None  # For timer completion
        
    def start_stopwatch(self):
        self.mode = 'stopwatch'
        if not self.running:
            self.running = True
            self.timer_event = Clock.schedule_interval(self.update_stopwatch, 0.1)
    
    def update_stopwatch(self, dt):
        self.time += dt
        
    def start_timer(self, hours=0, minutes=0, seconds=0, callback=None):
        self.mode = 'timer'
        self.time = hours * 3600 + minutes * 60 + seconds
        self.callback = callback
        if not self.running and self.time > 0:
            self.running = True
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)
    
    def update_timer(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.time = 0
            self.stop()
            if self.callback:
                self.callback()
    
    def stop(self):
        if self.running:
            self.running = False
            if self.timer_event:
                self.timer_event.cancel()
    
    def reset(self):
        self.stop()
        self.time = 0
        
    def get_time_string(self):
        minutes, seconds = divmod(int(self.time), 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"