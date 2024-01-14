import requests
import config
import api
import datetime

class ForecastWeather5d:
    def __init__(self, city_name: str):
        self.__URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
        self.__API_KEY = config.API_KEY
        self.city = city_name

    def get_info_to_weather_5d(self):
        PARAMETERS = dict(apikey=self.__API_KEY, language="ru")

        session = requests.session()
        response = session.get(self.__URL + api.cities.get(self.city)[0], params=PARAMETERS)
        information_weather_5d: list = list()
        if response.status_code == 200:
            for info_day in response.json()["DailyForecasts"]:
                list_weather_1d = {
                    "Date": info_day.get("Date")[:10],
                    "Temperature": [api.convert_fr_to_cl(info_day.get("Temperature")["Minimum"]["Value"]), api.convert_fr_to_cl(info_day.get("Temperature")["Maximum"]["Value"])],
                    "Day": info_day.get("Day")["IconPhrase"],
                    "Night": info_day.get("Night")["IconPhrase"]
                }
                information_weather_5d.append(list_weather_1d)
        return information_weather_5d


    def __repr__(self):
        return f"{self.city}: weather_5_day"