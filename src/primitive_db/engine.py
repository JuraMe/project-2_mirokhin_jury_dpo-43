import shlex
from prettytable import PrettyTable
from primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data
from primitive_db.core import create_table, drop_table, insert, select, update, delete
from primitive_db.parser import parse_where_clause, parse_set_clause
from primitive_db.constants import META_FILE

# Функция помощи
def print_help() -> None:
    print("\n*** Управление таблицами ***")
    print("Функции:")
    print("<command> create_table <имя> <столбец1:тип> ... - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя> - удалить таблицу")

    print("\n*** Работа с данными (CRUD) ***")
    print("<command> insert <таблица> <значение1> <значение2> ... - добавить запись")
    print("<command> select <таблица> [WHERE условие] - выбрать записи")
    print("<command> update <таблица> SET поле=значение WHERE условие - обновить записи")
    print("<command> delete <таблица> WHERE условие - удалить записи")
    print("\nПримеры:")
    print('  insert users "John" 28 true')
    print('  select users')
    print('  select users WHERE age = 28')
    print('  update users SET age = 30 WHERE name = "John"')
    print('  delete users WHERE ID = 1')

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

        elif command == "insert":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы и значения.")
                continue

            table_name = args[1]
            values = args[2:]
            insert(metadata, table_name, values)

        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")