# api.py

import json

from src.setings import Setings
from src.storage import Storage
from src.selector import Selector

# from setings import Setings
# from storage import Storage
# from selector import Selector

from duckduckgo_search import DDGS
import requests
import base64


class Api:
    """
    Модуль Api:
    - Объявление методов для работы с PY приложением
    """

    def __init__(self) -> list:
        self.setings = Setings()
        self.storage = Storage()
        self.selector = Selector()


api = Api()


def get_high_quality_image(query: str) -> str:
    """
    Возвращает ссылку на фото в высоком качестве по запросу.
    Использует DuckDuckGo Images (без API-ключей).
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(f"{query} poster", max_results=1))
            if not results:
                return "Не найдено изображений."

            return results[0]["image"]
    except:
        return ""

def get_all_games():
    res = api.storage.get(api.setings.COMPUTERS_JSON_FILE)
    for item in res:
        if "url" not in item or item["url"] == "":
            item["url"] = get_high_quality_image(item["name"])
        if "image_binary" not in item or item["image_binary"] == "":
            try:
                img_data = requests.get(item["url"]).content
                item["image_binary"] = base64.b64encode(
                    img_data
                ).decode("utf-8")
            except Exception:
                item["image_binary"] = None

    api.storage.set(api.setings.COMPUTERS_JSON_FILE, res)
    return json.dumps(res)


def handle_event(event_json: str) -> str:
    data = json.loads(event_json)
    match data["path"]["name"]:
        case "game":
            match data["path"]["type"]:
                case "get":
                    return get_all_games()
                case "content":
                    api.selector.run(data["path"]["content"])
                    
    result = {"status": "ok", "from": "Python", "echo": data}
    return json.dumps(result)


# api.selector.run('stellar-blade')
# input()