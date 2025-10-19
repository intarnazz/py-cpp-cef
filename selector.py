# selector.py

import time
from InquirerPy import inquirer
from setings import Setings
from storage import Storage
# from checker import Checker


class Selector:
    """
    Модуль выбора данных:
    - Интерактивный выбор пути поиска (InquirerPy)
    - Обновление порядка элементов в JSON
    """

    def __init__(self) -> list:
        self.setings = Setings()
        self.storage = Storage()
        # self.checker = Checker()

    def select(self) -> list:
        """
        Дает пользователю выбрать путь для поиска.
        Если выбран "Проверять все" — возвращает весь список.
        Если выбран конкретный путь — перемещает его в начало и обновляет JSON.

        :return: список выбранных элементов (всегда список, даже если один элемент)
        """
        computers = self.storage.get(self.setings.COMPUTERS_JSON_FILE)

        choices = [computer["path"] for computer in computers]
        choices.insert(0, "🔎 Проверять все")

        selected = inquirer.select(
            message="Выберите путь для поиска:",
            choices=choices,
            default="🔎 Проверять все",
        ).execute()

        if selected == "🔎 Проверять все":
            return computers
        else:
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

    # def run(self) -> bool:
    #     """
    #     Запуск запуск терминала.

    #     :return: bool
    #     """
    #     try:
    #         found = self.checker.check(self.select())
    #         if not found:
    #             print("\n❌ Ничего не найдено.")
    #             input(
    #                 "Нажмите Enter, чтобы вернуться к выбору пути, "
    #                 "или подождите 60 секунд...\n"
    #             )
    #             return False
    #         else:
    #             # если найдено — возвращаемся к выбору
    #             return False
    #     except Exception as e:
    #         print(f"Ошибка: {e}")

    #     time.sleep(10)
    #     return True
