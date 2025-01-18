import requests
from config import GISMETEO_TOKEN as TOKEN
from requests.utils import quote

def get_temperature(city):
    # Замените 'your_api_url' на настоящий URL API Gismeteo
    headers = {
    'X-Gismeteo-Token': TOKEN,
    'Accept-Encoding': 'gzip'
}

    url = 'https://api.gismeteo.net/v2/search/cities/?lang=ru&query='

    city = quote(city)

    # Выполняем GET-запрос
    response = requests.get(url + city, headers=headers)
    # Проверяем, успешен ли запрос
    response.raise_for_status()
    # Получаем данные из ответа
    data = response.json()
    # Извлекаем информацию о температуре
    temperature = data['current']['temperature']
    return temperature

print(get_temperature('Санкт-Петербург'))