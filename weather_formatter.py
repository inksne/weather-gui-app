from weather_api_service import Weather

def format_weather(weather: Weather) -> str:
    '''Форматирует данные о погоде в строку'''
    return (f"{weather.city}, температура {weather.temperature}°C, "
            f"{weather.weather_type.value}\n"
            f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
            f"Закат: {weather.sunset.strftime('%H:%M')}\n")


if __name__ == "__main__":
    from datetime import datetime
    from weather_api_service import WeatherType
    print(format_weather(Weather(
        temperature=25,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime.fromisoformat("2024-09-29 04:00:00"),
        sunset=(datetime.fromisoformat("2024-09-29 20:25:00")),
        city="Moscow"
    )))