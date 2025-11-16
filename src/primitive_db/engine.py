import shlex
from primitive_db.utils import load_metadata, save_metadata
from primitive_db.core import create_table, drop_table

META_FILE = "db_meta.json"

# Функция помощи
def print_help() -> None:
    print("\n*** Управление таблицами ***")
    print("Функции:")
    print("<command> create_table <имя> <столбец1:тип> ... - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя> - удалить таблицу")

    print("\n*** Общие команды ***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация\n")

# Главный цикл работы программы
def run() -> None:
    metadata = load_metadata(META_FILE)

    print("\n*** База данных запущена ***")
    print_help()

    while True:
        try:
            user_input = input("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы...")
            break

        if not user_input:
            continue

        args = shlex.split(user_input)  #Для надежного разбора строки shlex
        command = args[0]

        if command == "exit":
            print("Выход из программы...")
            break

        elif command == "help":
            print_help()

        elif command == "list_tables":
            if metadata:
                for table in metadata.keys():
                    print("-", table)
            else:
                print("Таблиц пока нет.")

        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: недостаточно аргументов.")
                continue

            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)

        elif command == "drop_table":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILE, metadata)

        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")