# selector.py

import time
from InquirerPy import inquirer
from src.setings import Setings
from src.storage import Storage
from src.checker import Checker


class Selector:
    """
    Модуль выбора данных:
    - Интерактивный выбор пути поиска (InquirerPy)
    - Обновление порядка элементов в JSON
    """

    def __init__(self) -> list:
        self.setings = Setings()
        self.storage = Storage()
        self.checker = Checker()

    def select(self, content) -> list:
        """
        Дает пользователю выбрать путь для поиска.
        Если выбран "Проверять все" — возвращает весь список.
        Если выбран конкретный путь — перемещает его в начало и обновляет JSON.

        :return: список выбранных элементов (всегда список, даже если один элемент)
        """
        computers = self.storage.get(self.setings.COMPUTERS_JSON_FILE)
        selected = content

        paths = [c.get("path") for c in computers if "path" in c]
        if selected not in paths:
            return False, 'Не верный Path в Selected'

        # перемещаем выбранный объект в начало
        selected_computer = next(
            (computer for computer in computers if computer["path"] == selected),
            None,
        )
        if selected_computer:
            computers.remove(selected_computer)
            computers.insert(0, selected_computer)

            # сохраняем обновлённый порядок
            self.storage.set(self.setings.COMPUTERS_JSON_FILE, computers)

        return [selected_computer] if selected_computer else []

    def run(self, content) -> bool:
        """
        Запуск терминала.

        :return: bool
        """
        try:
            result = self.select(content)
            found = self.checker.check(result)

            if not found:
                return False
            else:
                return True
        except Exception as e:
            print(f"Ошибка: {e}")

        return False
