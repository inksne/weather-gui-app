from datetime import datetime
from pathlib import Path
from typing import TypedDict
from abc import abstractmethod
import json

from weather_api_service import Weather
from weather_formatter import format_weather


class WeatherStorage:
    '''Базовый класс для хранилища погоды'''
    @abstractmethod
    def save(self, weather: Weather):
        pass


class PlainFileWeatherStorage(WeatherStorage):
    '''История погоды в текстовом файле'''
    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self._file, "a") as f:
            f.write(f"{now}\n{formatted_weather}")


class HistoryRecord(TypedDict):
    date: str
    weather: str


class JSONFileWeatherStorage(WeatherStorage):
    '''Хранилище с JSON файлом'''
    def __init__(self, jsonfile: Path):
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, weather: Weather) -> None:
        history = self._read_history()
        history.append({
            "date": str(datetime.now()),
            "weather": format_weather(weather),
        })
        self._write(history)

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def _read_history(self) -> list[HistoryRecord]:
        with open(self._jsonfile, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, history: list[HistoryRecord]) -> None:
        with open(self._jsonfile, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    '''Сохраняет погоду в хранилище'''
    storage.save(weather)