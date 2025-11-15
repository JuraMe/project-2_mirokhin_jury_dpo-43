import prompt

def welcome():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "exit":
            print("Выход из программы")
            break
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {command}")


# Функция помощи
def print_help() -> None:
    print("\n*** Управление таблицами ***")
    print("Функции:")
    print("<command> create_table <имя> <столбец1:тип> ... - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя> - удалить таблицу")

    print("\n*** Операции с данными (CRUD) ***")
    print("Функции:")
    print("<command> insert into <имя> values (<v1>, <v2>, ...)")
    print("  - добавить запись в таблицу")
    print("<command> select from <имя> [where <столбец>=<значение>]")
    print("  - выбрать записи")
    print("<command> update <имя> set <столбец>=<значение>")
    print("  where <столбец>=<значение> - обновить записи")
    print("<command> delete from <имя> where <столбец>=<значение>")
    print("  - удалить запись")
    print("<command> info <имя> - информация о таблице")

    print("\n*** Общие команды ***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация\n")