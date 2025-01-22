import requests
from config import CHAD_API_KEY as TOKEN
import re

def get_food_info(food):
    # Формируем запрос
    request_json = {
        "message": f"Сколько в среднем каллорий в 100 граммах {food}. В ответе нужно только число, округленное до целых, без других символов",
        "api_key": TOKEN
    }

    # Отправляем запрос и дожидаемся ответа
    response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini',
                             json=request_json)

    # Проверяем, отправился ли запрос
    if response.status_code != 200:
        print(f'Ошибка! Код http-ответа: {response.status_code}')
    else:
        # Получаем текст ответа и преобразовываем в dict
        resp_json = response.json()

        # Если успешен ответ, то выводим
        if resp_json['is_success']:
            resp_msg = resp_json['response']
            used_words = resp_json['used_words_count']
            return re.sub(r'\D', '', resp_msg)
        else:
            error = resp_json['error_message']
            print(f'Ошибка: {error}')

def get_workout_info(food):
    # Формируем запрос
    request_json = {
        "message": f"Сколько каллорий в среднем тратится за одну минуту выполнения упражнения: {food}. В ответе нужно только число, округленное до целых, без других символов",
        "api_key": TOKEN
    }

    # Отправляем запрос и дожидаемся ответа
    response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini',
                             json=request_json)

    # Проверяем, отправился ли запрос
    if response.status_code != 200:
        print(f'Ошибка! Код http-ответа: {response.status_code}')
    else:
        # Получаем текст ответа и преобразовываем в dict
        resp_json = response.json()

        # Если успешен ответ, то выводим
        if resp_json['is_success']:
            resp_msg = resp_json['response']
            used_words = resp_json['used_words_count']
            return re.sub(r'\D', '', resp_msg)
        else:
            error = resp_json['error_message']
            print(f'Ошибка: {error}')