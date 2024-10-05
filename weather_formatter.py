from weather_api_service import Weather

def format_weather(weather: Weather) -> str:
    '''Форматирует данные о погоде в строку'''
    return (f"{weather.city}, температура {weather.temperature}°C, "
            f"{weather.weather_type}, скорость ветра {weather.wind} м/с")


if __name__ == "__main__":
    print(format_weather(Weather(
        temperature=25,
        weather_type='Ясно',
        city="Москва",
        wind=4
    )))