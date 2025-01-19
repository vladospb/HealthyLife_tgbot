import requests
from config import OPENWHEATHER_TOKEN as TOKEN

DEFAULT_CITY = 'Saint Petersburg'

def get_temperature(city):
    city_id = 0
    if city in (None, 'None', 0, '0', ''):
        city = DEFAULT_CITY
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': TOKEN})
        data = res.json()
        city_id = data['list'][0]['id']
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                         params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': TOKEN})
            data = res.json()
            return data['main']['temp']
        except Exception as e:
            print("Exception (weather):", e)
            pass
    except Exception as e:
        print("Exception (find):", e)
    pass