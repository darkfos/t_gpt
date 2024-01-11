import requests
import config


class City:
    def __init__(self, name_city: str):
        self.__API_KEY = config.API_KEY
        self.__API_KEY_GEO = config.API_KEY_GEO
        self.__URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
        self.__URL_ab_city = "https://api.geotree.ru/search.php"
        self.name_city = name_city

    def api_get_info_of_city(self) -> tuple | None:

        parameters: dict = {
            "apikey": self.__API_KEY,
            "q": self.name_city,
            "language": "ru"
        }

        parameters_to_geo: dict = {
            "key": self.__API_KEY_GEO,
            "term": self.name_city
        }
        request = requests.get(url=self.__URL, params=parameters).json()
        request_to_get = requests.get(url=self.__URL_ab_city, params=parameters_to_geo).json()
        print(request_to_get)
        try:
            type_colony: str = request[0]["Type"]
            region: str = request[0]["Region"]["LocalizedName"]
            country: str = request[0]["Country"]["LocalizedName"]
            type_localization: str = request[0]["AdministrativeArea"]["LocalizedType"]
            population_of_city: str = str(request_to_get[0]["population"]) + " чел."
            area_city: str = str(request_to_get[0]["area"]) + " км2."
            time_zone: str = request[0]["TimeZone"]["Name"] + "\n\n"
            latitude_city: str = str(request[0]["GeoPosition"]["Latitude"])
            longtitude_city: str = str(request[0]["GeoPosition"]["Longitude"])
        except Exception:
            return None

        return type_colony, region, country, type_localization, population_of_city, time_zone, area_city, latitude_city, longtitude_city

    def __name__(self) -> str:
        return "City"

    def __repr__(self):
        return "Класс для получения информации о городе"

    def __del__(self):
        print(f"Объект: {self.__name__()} был удалён.")
