from typing import NamedTuple
from geopy.geocoders import Nominatim

from config import USE_ROUNDED_COORDS
from exceptions import CantGetCoordinates

class Coordinates(NamedTuple):
    latitude: float
    longitude: float

def get_coordinates(city: str):
    '''Возвращает координаты города по его названию'''
    try:
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(city)
        latitude = getLoc.latitude
        longitude = getLoc.longitude
        if USE_ROUNDED_COORDS:
            latitude, longitude = map(lambda c: round(c, 1), [latitude, longitude])
        return Coordinates(latitude=latitude, longitude=longitude)
    except CantGetCoordinates:
        print('Не удалось получить координаты')
        raise CantGetCoordinates
