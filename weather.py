from coordinates import get_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from pathlib import Path

from exceptions import ApiServiceError, CantGetCoordinates
from history import save_weather, JSONFileWeatherStorage

def main():
    try:
        coordinates = get_coordinates()
    except CantGetCoordinates:
        print('Не удалось получить координаты')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(f'Не удалось получить погоду по координатам {coordinates}')
        exit(1)
    print(format_weather(weather))

    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / "history.json")
    )

if __name__ == '__main__':
    main()