import requests
import config


class City:
    def __init__(self, name_city: str):
        self.__API_KEY = config.API_KEY
        self.__URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
        self.name_city = name_city

    def api_get_info_of_city(self) -> tuple | None:
        print(self.__API_KEY, self.name_city)
        parameters: dict = {
            "apikey": self.__API_KEY,
            "q": self.name_city,
            "language": "ru"
        }
        request = requests.get(url=self.__URL, params=parameters).json()
        try:
            type_colony: str = request[0]["Type"]
            region: str = request[0]["Region"]["LocalizedName"]
            country: str = request[0]["Country"]["LocalizedName"]
            type_localization: str = request[0]["AdministrativeArea"]["LocalizedType"]
            time_zone: str = request[0]["TimeZone"]["Name"]
        except Exception:
            return None

        return type_colony, region, country, type_localization, time_zone

    def __name__(self) -> str:
        return "Город: " + self.name_city

