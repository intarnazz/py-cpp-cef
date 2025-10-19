# setings.py

import os
# import json
from dotenv import load_dotenv


class Setings:
    """
    Модуль инициализации приложения:
    - Импорт внешних библиотек
    - Загрузка .env переменных
    - Инициализация pygame
    - Определение констант и заголовков HEADERS
    """

    def __init__(self):
        # Загружаем переменные окружения из .env
        load_dotenv()

        # Константы
        self.BASE_URL = "https://fogplay.mts.ru"
        self.COMPUTER_URL = f"{self.BASE_URL}/computer/"
        # self.AUDIO_FILE = "./src/sound/bonfire.mp3"
        self.AUDIO_FILE = "./src/sound/item.mp3"
        self.COMPUTERS_JSON_FILE = "./src/storage/computers.json"

        # Заголовки из .env
        self.HEADERS = os.getenv("HEADERS")

# s = Setings()
# print(s.HEADERS)
