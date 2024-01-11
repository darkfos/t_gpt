from configparser import ConfigParser

config = ConfigParser()
config.read("weather_configs.ini")

API_KEY = config.get("auth", "API_KEY")
API_KEY_GEO = config.get("auth", "API_KEY_GEO")
TG_API_KEY = config.get("auth", "TG_API_KEY")
SQL_ALCHEMY_URL = config.get("urls", "SQL_LITE_URL")