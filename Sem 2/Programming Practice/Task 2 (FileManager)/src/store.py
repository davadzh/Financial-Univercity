import pathlib


class Store:
    """Хранилище"""

    def __init__(self, sep: str) -> None:
        self.sep = sep
        self.__storage = ["storage"]

    def to_path(self, path: str) -> None:
        """Добавляет файл в иерархию каталогов"""
        # cd ..
        if ".." in path and len(self.__storage) != 1:
            self.__storage.pop(-1)
        # cd .. (ошибка)
        elif ".." in path:
            print("Невозможно выйти за пределы окружения.")
        # cd [path]
        else:
            self.__storage.append(path)

    def file_to_path(self, file_name: str) -> str:
        """Возвращает указанный файл в текущей иерархии каталогов"""
        local_storage = self.__storage.copy()
        local_storage.append(file_name)
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + self.sep + self.sep.join(local_storage)

    @property
    def path(self):
        """Возвращает текущую иерархию каталогов"""
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + self.sep + self.sep.join(self.__storage)

    @property
    def upper_path(self):
        """Возвращает директорию выше текущей"""
        abs_path = pathlib.Path(__file__).parent.absolute()
        print(self.__storage[1:])
        return str(abs_path) + self.sep + self.sep.join(self.__storage[:1])
