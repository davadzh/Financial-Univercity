from typing import Dict
import os
from store import Store
import shutil


class Manager:
    """Файловый менеджер"""

    def __init__(self) -> None:
        self.sep = os.sep
        self.storage = Store(self.sep)

    @staticmethod
    def get_commands() -> Dict[str, str]:
        """Получает список всех команд"""

        commands_dict = {
            "cd": "Перемещение между папками",
            "ls": "Вывод содержимого текущей папки на экран",
            "mkdir": "Создание папки",
            "rmdir": "Удаление папки",
            "create": "Создание файла",
            "rename": "Переименование файла/папки",
            "read": "Чтение файла",
            "remove": "Удаление файла",
            "copy": "Копирование файла/папки",
            "move": "Перемещение файла/папки",
            "write": "Запись в файл",
        }

        return commands_dict

    def mkdir(self, filename: str):
        """Создание папки (с указанием имени)"""
        current_path = self.storage.file_to_path(filename)
        try:
            os.mkdir(current_path)
        except FileNotFoundError:
            os.makedirs(current_path)
        except FileExistsError:
            print(f"Директория {filename} уже существует")

    def rmdir(self, filename: str):
        """Удаление папки по имени"""
        current_path = self.storage.file_to_path(filename)
        try:
            os.rmdir(current_path)
        except OSError:
            try:
                shutil.rmtree(current_path, ignore_errors=False, onerror=None)
            except FileNotFoundError:
                print(f"Директории {filename} не существует")
            except NotADirectoryError:
                print(f"Файл {filename} не является директорией")

    def cd(self, filename: str):
        """
        Перемещение между папками
        - заход в папку по имени
        - выход на уровень вверх
        - в пределах рабочей папки
        """
        self.storage.to_path(filename)
        current_path = self.storage.path

        try:
            os.chdir(current_path)
        except NotADirectoryError:
            self.storage.to_path(f"..{self.sep}")
            print(f"Файл {filename} не является директорией")
        except FileNotFoundError:
            self.storage.to_path(f"..{self.sep}")
            print(f"Директории {filename} не существует")

    def ls(self):
        """
        Вывод содержимого текущей директории на экран
        """
        current_path = self.storage.path
        filelist = os.listdir(current_path)
        for i in range(len(filelist)):
            if os.path.isdir(self.storage.file_to_path(filelist[i])):
                filelist[i] = f"[dir] {filelist[i]}"
            elif os.path.isfile(self.storage.file_to_path(filelist[i])):
                filelist[i] = f"[file] {filelist[i]}"

        r = "\n".join(filelist)
        print(f"Содержимое {current_path}:\n{r}")

    def touch(self, filename: str):
        """Создание пустых файлов с указанием имени"""
        current_path = self.storage.file_to_path(filename)
        try:
            open(current_path, "a").close()
        except IsADirectoryError:
            print(f"Файл {filename} уже был создан и это директория")

    def cat(self, filename: str) -> str:
        """Просмотр содержимого текстового файла"""
        current_path = self.storage.file_to_path(filename)
        try:
            with open(current_path, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except IsADirectoryError:
            print(f"Файл {filename} является директорией")

    def rename(self, filename_old: str, filename_new: str):
        """Переименование файлов"""

        path_old = self.storage.file_to_path(filename_old)
        path_new = self.storage.file_to_path(filename_new)

        # Проверка на то, чтоб файл с новым именем не существовал
        try:
            if not os.path.isfile(path_new):
                os.rename(path_old, path_new)
            else:
                raise IsADirectoryError
        except FileNotFoundError:
            print(f"Указанного файла {filename_old} не существует")
        except IsADirectoryError:
            print(f"Файл с названием {filename_new} уже существует")

    def rm(self, filename: str):
        """Удаление файлов по имени"""
        path = self.storage.file_to_path(filename)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f"Файла {filename} не существует")

    def cp(self, filename: str, path: str):
        """Копирование файлов из одной папки в другую"""
        path_old = self.storage.file_to_path(filename)
        # Копирование на уровень выше
        if ".." in path:
            path_new = self.storage.upper_path + self.sep + filename
        else:
            # Проверяем на то, что это за тип файла
            buff = self.storage.file_to_path(path)

            # Если конечный путь папка - закидываем туда файл
            if os.path.isdir(buff):
                path_new = self.storage.file_to_path(path + self.sep + filename)
            else:
                # Значит это копирование на одном уровне
                path_new = self.storage.file_to_path(path)
        try:
            shutil.copyfile(path_old, path_new)
        # Если это директория - копируем директорию
        except IsADirectoryError:
            shutil.copytree(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def mv(self, filename: str, path: str):
        """Перемещение файлов"""
        path_old = self.storage.file_to_path(filename)
        if ".." in path:
            path_new = self.storage.upper_path + self.sep + filename
        else:
            # Проверяем на то, что это за тип файла
            buff = self.storage.file_to_path(path)
            # Если директория - закидываем туда файл
            if os.path.isdir(buff):
                path_new = self.storage.file_to_path(path + self.sep + filename)
            else:
                # Значит это перемещение на одном уровне
                path_new = self.storage.file_to_path(path)
        try:
            shutil.move(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def write(self, filename: str, *data: str):
        """Запись текста в файл"""
        text = " ".join(data)
        path = self.storage.file_to_path(filename)
        try:
            with open(path, "a") as file:
                file.write(text)
        except IsADirectoryError:
            print(f"Указанный файл {filename} является директорией")

    def router(self, command: str):
        """Ассоциация между командами и методами FileProcessing"""

        commands = [
            self.cd,
            self.ls,
            self.mkdir,
            self.rmdir,
            self.touch,
            self.rename,
            self.cat,
            self.rm,
            self.cp,
            self.mv,
            self.write,
        ]
        item_dict = dict(zip(Manager.get_commands().keys(), commands))
        return item_dict.get(command, None)

    @staticmethod
    def get_formatted_commands() -> str:
        """Получение всех команд в отформатированном виде"""
        return "\n".join(
            [
                f"{key} - {value}"
                for (key, value) in Manager.get_commands().items()
            ]
        )
