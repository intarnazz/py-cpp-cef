# parser.py

from bs4 import BeautifulSoup
from src.setings import Setings


class Parser:
    """
    Модуль для парсинга HTML:
    - Извлечение ссылок на игры по коду
    """

    def __init__(self):
        self.setings = Setings()

    def pars(self, html: str, target_code: str) -> str | None:
        """
        Ищет в HTML карточку с нужным кодом и возвращает ссылку для запуска игры.

        :param html: HTML-код страницы
        :param target_code: код игры (строка для поиска)
        :return: ссылка для запуска игры или None
        """
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", class_="card")

        for card in cards:
            title = card.find("p", class_="card__title")
            if title and target_code in title.text:
                play_button = card.find("a", class_="button js-play")
                if play_button and "href" in play_button.attrs:
                    return f'{self.setings.BASE_URL}{play_button["href"]}'

        return None
