from typing import NamedTuple
from geopy.geocoders import Nominatim

from config import USE_ROUNDED_COORDS
from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


getlocation = input('Введите город:')


def get_coordinates():
    '''Возвращает координаты, используя Windows GPS'''
    try:
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(getlocation)
        latitude = getLoc.latitude
        longitude = getLoc.longitude
        if USE_ROUNDED_COORDS:
            latitude, longitude = map(lambda c: round(c, 1), [latitude, longitude])
        return Coordinates(latitude=latitude, longitude=longitude)
    except CantGetCoordinates:
        print('Не удалось получить координаты')


if __name__ == '__main__':
    print(get_coordinates())