from manager import Manager


def start():
    # Менеджер файлов
    manager = Manager()

    print("Добро пожаловать в файловый менеджер!\n"
          f"Список доступных команд:\n{Manager.get_formatted_commands()}")

    # Начало программы
    while True:

        command = input("\nFileManager: ").split(" ")

        # Выход
        if command[0] == "exit":
            break

        # Получаем команду
        res = manager.router(command[0])

        if res:
            try:
                res(*command[1:])
            except TypeError:
                print(f"Команда {command[0]} была использована некорректно")

        else:
            print(f"Команды {command[0]} не существует.\n"
                  f"Список команд:\n{Manager.get_formatted_commands()}")

    print("Вы вышли из файлового менеджера.")


if __name__ == "__main__":
    start()
