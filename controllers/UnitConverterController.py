class UnitConverterController:
    def __init__(self, app):
        self.app = app
        self.root = None  # This will be set to the root of the app later
        
        # Conversion dictionaries
        self.length_conversions = {
            "inches": 0.0254,
            "feet": 0.3048,
            "yards": 0.9144,
            "meters": 1.0,
            "kilometers": 1000.0,
            "miles": 1609.34
        }
        
        self.volume_conversions = {
            "milliliters": 0.001,
            "liters": 1.0,
            "cups": 0.236588,
            "pints": 0.473176,
            "quarts": 0.946353,
            "gallons": 3.78541
        }
        
        self.time_conversions = {
            "seconds": 1.0,
            "minutes": 60.0,
            "hours": 3600.0,
            "days": 86400.0,
            "weeks": 604800.0,
            "months": 2629746.0,  # Average month
            "years": 31556952.0   # Average year
        }
    
    def convert_units(self, measurement_type, from_unit, to_unit, value):
        """Convert between units based on measurement type"""
        try:
            value = float(value)
        except (ValueError, TypeError):
            return "Invalid input"
        
        if measurement_type == "length":
            return self.convert_length(from_unit, to_unit, value)
        elif measurement_type == "volume":
            return self.convert_volume(from_unit, to_unit, value)
        elif measurement_type == "time":
            return self.convert_time(from_unit, to_unit, value)
        else:
            return "Select measurement type"
    
    def convert_length(self, from_unit, to_unit, value):
        """Convert length units"""
        # Convert to meters first, then to target unit
        if from_unit not in self.length_conversions or to_unit not in self.length_conversions:
            return "Invalid unit"
        
        meters = value * self.length_conversions[from_unit]
        result = meters / self.length_conversions[to_unit]
        return f"{result:.4f}".rstrip('0').rstrip('.') if '.' in f"{result:.4f}" else f"{result:.4f}"
    
    def convert_volume(self, from_unit, to_unit, value):
        """Convert volume units"""
        # Convert to liters first, then to target unit
        if from_unit not in self.volume_conversions or to_unit not in self.volume_conversions:
            return "Invalid unit"
        
        liters = value * self.volume_conversions[from_unit]
        result = liters / self.volume_conversions[to_unit]
        return f"{result:.4f}".rstrip('0').rstrip('.') if '.' in f"{result:.4f}" else f"{result:.4f}"
    
    def convert_time(self, from_unit, to_unit, value):
        """Convert time units"""
        # Convert to seconds first, then to target unit
        if from_unit not in self.time_conversions or to_unit not in self.time_conversions:
            return "Invalid unit"
        
        seconds = value * self.time_conversions[from_unit]
        result = seconds / self.time_conversions[to_unit]
        return f"{result:.4f}".rstrip('0').rstrip('.') if '.' in f"{result:.4f}" else f"{result:.4f}"
    
    def get_available_units(self, measurement_type):
        """Get list of available units for a measurement type"""
        if measurement_type == "length":
            return list(self.length_conversions.keys())
        elif measurement_type == "volume":
            return list(self.volume_conversions.keys())
        elif measurement_type == "time":
            return list(self.time_conversions.keys())
        else:
            return []
