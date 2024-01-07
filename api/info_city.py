import requests
import config


class City:
    def __init__(self, name_city: str):
        self.__URL = ""
        self.__API_KEY = config.API_KEY
        self.name_city = name_city

    def api_get_info_of_city(self) -> dict:
        request = requests.get(url=self.__URL + self.name_city).json()
        return dict()

    def __name__(self) -> str:
        return "Город: " + self.name_city
