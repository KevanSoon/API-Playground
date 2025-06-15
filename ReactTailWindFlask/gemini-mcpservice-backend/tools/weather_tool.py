# server/tools/weather_tool.py
import random
import requests
          

def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """
    Simulates fetching weather for a given location.
    In a real application, this would call a weather API.
    """
    print(f"TOOL SERVER: Called get_current_weather for {location} with unit {unit}")
    
    # Simulate some weather data
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Snowy"]
    temp_c = random.randint(-5, 35)
    
    if unit == "fahrenheit":
        temp = (temp_c * 9/5) + 32
        unit_symbol = "°F"
    else:
        temp = temp_c
        unit_symbol = "°C"
        
    weather_info = {
        "location": location,
        "temperature": f"{temp:.1f}{unit_symbol}",
        "condition": random.choice(conditions),
        "unit_used": unit
    }

  
        
    print(f"TOOL SERVER: Responding with: {weather_info}")
    return weather_info
    