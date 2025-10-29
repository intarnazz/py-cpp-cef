# checker.py

import requests
import webbrowser
from InquirerPy import inquirer

from src.setings import Setings
from src.parser import Parser
# from audio import Audio


class Checker:
    """
    Модуль проверки ссылок:
    - Обходит страницы каталога
    - Ищет коды игр
    - При нахождении воспроизводит звук и предлагает действие пользователю
    """

    def __init__(self):
        # self.audio = Audio()
        self.parser = Parser()
        self.setings = Setings()

    def check(self, data: list) -> bool:
        """
        Проверяет наличие указанных кодов на страницах.

        :param data: список объектов вида {"path": ..., "code": ...}
        :return: True, если найдена хотя бы одна ссылка, иначе False
        """

        for item in data:
            path = item.get("path")
            codes = item.get("code")

            if isinstance(codes, str):
                codes = [codes]
            if not path or not codes:
                continue

            # проверяем первые две страницы
            for page in range(1, 5):
                url = f"{self.setings.COMPUTER_URL}{path}/?slug={path}&page={page}"

                try:
                    print(f"🔎 Проверка {url} ...")
                    response = requests.get(
                        url, headers=self.setings.HEADERS, timeout=10
                    )
                    response.raise_for_status()
                    html = response.text

                    for code in codes:
                        if code in html:
                            play_url = self.parser.pars(html, code)
                            if play_url:
                                print(f"\n🔔 НАЙДЕНО: {code} на {url}")

                                # звук
                                # self.audio.play()

                                # выбор действия
                                choice = "▶ Открыть ссылку"

                                # self.audio.stop()

                                if choice == "▶ Открыть ссылку":
                                    webbrowser.open(play_url)

                                return True
                except Exception as e:
                    print(f"Ошибка при запросе {url}: {e}")

        return False
