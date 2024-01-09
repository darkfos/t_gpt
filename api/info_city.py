import requests
import config


class City:
    def __init__(self, name_city: str):
        self.__URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
        self.__API_KEY = config.API_KEY
        self.name_city = name_city

    def api_get_info_of_city(self, name_city: str) -> tuple:
        parameters: dict = {
            "apikey": self.__API_KEY,
            "q": name_city,
            "language": "ru"
        }
        request = requests.get(url=self.__URL + self.name_city).json()

        type_colony: str = request.get("Type")
        region: str = request["Region"]["LocalizedName"]
        country: str = request["Country"]["LocalizedName"]
        type_localization: str = request["AdministrativeArea"]["LocalizedType"]
        time_zone: str = request["TimeZone"]["Name"]

        return type_colony, region, country, type_localization, time_zone

    def __name__(self) -> str:
        return "Город: " + self.name_city
