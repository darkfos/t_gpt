import requests
import config
import api


class CityNeighbors:
    def __init__(self, name_city: str):
        self.__URL = "http://dataservice.accuweather.com/locations/v1/cities/neighbors/"
        self.__API_KEY = config.API_KEY
        self.code_city: str = api.cities[name_city][0]

    def get_neighbors_city(self) -> list:
        parameters = {
            "apikey": self.__API_KEY,
            "language": "ru"
        }

        request = requests.get(self.__URL + self.code_city, params=parameters).json()
        all_neighbors_city: list = [city_name["LocalizedName"] for city_name in request]

        return all_neighbors_city

    def __repr__(self):
        return "Код города: %s" % self.code_city
