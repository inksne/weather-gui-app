USE_ROUNDED_COORDS = True
OPENWEATHER_API = "e49676dc4ef67ecede4f6823ee1ff6d0"
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&"
    "units=metric"
)