from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, ListProperty

class UnitConverterScreen(Screen):
    measurement_type = StringProperty("none")
    unit_options = ListProperty([])
    controller = ObjectProperty(None)
    
    def on_measurement_type_change(self, spinner, text):
        """Called when measurement type spinner changes"""
        self.measurement_type = text
        self.update_conversion_options()
    
    def update_conversion_options(self):
        """Dynamically update unit options for the selected type"""
        if self.controller:
            self.unit_options = self.controller.get_available_units(self.measurement_type)
        else:
            self.unit_options = []
    
    def convert_units(self, from_unit, to_unit, value):
        """Convert between units using the controller"""
        if not self.controller:
            return "Controller not available"
        
        return self.controller.convert_units(self.measurement_type, from_unit, to_unit, value)


    def handle_conversion(self):
        from_unit = self.ids.from_unit.text
        to_unit = self.ids.to_unit.text
        value = self.ids.unit_input.text

        if not self.controller:
            result = "Controller not available"
        else:
            result = self.controller.convert_units(self.measurement_type, from_unit, to_unit, value)

        self.ids.result_label.text = result

        
        #return self.controller.convert_units(self.measurement_type, from_unit, to_unit, value)