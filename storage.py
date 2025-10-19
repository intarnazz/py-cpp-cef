# storage.py

import json


class Storage:
    """
    Модуль для работы с локальным хранилищем данных (JSON).
    """

    def __init__(self):
        pass

    def get(self, file: str) -> list:
        """
        Загружает данные из JSON файла.

        :return: список объектов из файла
        """
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {file} не найден. Возвращаю пустой список.")
            return []
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON ({file}): {e}")
            return []

    def set(self, file: str, value: any) -> bool:
        """
        Сохроняет данные в JSON файл.

        :return: bool
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(value, f, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            print(f"Файл {file} не найден.")
            return False

        return True
