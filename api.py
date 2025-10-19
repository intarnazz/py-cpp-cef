# api.py

#pip install duckduckgo-search

import json

# from selector import Selector
from src.setings import Setings
from src.storage import Storage

from duckduckgo_search import DDGS


class Api:
    """
    Модуль Api:
    - Объявление методов для работы с PY приложением
    """

    def __init__(self) -> list:
        self.setings = Setings()
        self.storage = Storage()


api = Api()

def get_high_quality_image(query: str) -> str:
    """
    Возвращает ссылку на фото в высоком качестве по запросу.
    Использует DuckDuckGo Images (без API-ключей).
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))
            if not results:
                return "Не найдено изображений."
            
            return results[0]['image']
    except:
        return ''


def handle_event(event_json: str) -> str:
    data = json.loads(event_json)
    match data["path"]["name"]:
        case "game":
            match data["path"]["type"]:
                case "get":
                    res = api.storage.get(api.setings.COMPUTERS_JSON_FILE)

                    for item in res:
                        if "url" not in item or item["url"] == "":
                            item["url"] = get_high_quality_image(item["name"])

                    api.storage.set(api.setings.COMPUTERS_JSON_FILE, res)

                    return json.dumps(res)

    result = {"status": "ok", "from": "Python", "echo": data}
    return json.dumps(result)
