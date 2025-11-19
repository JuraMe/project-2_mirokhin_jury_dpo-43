import shlex

from prettytable import PrettyTable

from primitive_db.constants import META_FILE
from primitive_db.core import create_table, delete, drop_table, insert, select, update
from primitive_db.parser import parse_set_clause, parse_where_clause
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


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

        elif command == "select":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            table_name = args[1]

            # Проверяем существование таблицы
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            # Загружаем данные таблицы
            table_data = load_table_data(table_name)

            # Ищем WHERE в исходной строке команды
            where_clause = None
            if "WHERE" in user_input.upper():
                # Находим позицию WHERE в исходной строке
                where_idx = user_input.upper().index("WHERE")
                where_str = user_input[where_idx + 5:].strip()
                try:
                    where_clause = parse_where_clause(where_str)
                except ValueError as e:
                    print(f"Ошибка парсинга WHERE: {e}")
                    continue

            # Выполняем SELECT
            records = select(table_data, where_clause)

            # Выводим результаты с помощью PrettyTable
            if records:
                table = PrettyTable()
                # Используем ключи первой записи для заголовков
                table.field_names = list(records[0].keys())
                for record in records:
                    table.add_row([record.get(field) for field in table.field_names])
                print(table)
                print(f"\nНайдено записей: {len(records)}")
            else:
                print("Записей не найдено.")

        elif command == "update":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            table_name = args[1]

            # Проверяем существование таблицы
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            # Ищем SET и WHERE в исходной строке команды
            if "SET" not in user_input.upper():
                print("Ошибка: отсутствует SET условие.")
                continue

            if "WHERE" not in user_input.upper():
                print("Ошибка: отсутствует WHERE условие.")
                continue

            # Извлекаем SET и WHERE части
            set_idx = user_input.upper().index("SET")
            where_idx = user_input.upper().index("WHERE")

            if where_idx <= set_idx:
                print("Ошибка: WHERE должен идти после SET.")
                continue

            set_str = user_input[set_idx + 3:where_idx].strip()
            where_str = user_input[where_idx + 5:].strip()

            try:
                set_clause = parse_set_clause(set_str)
                where_clause = parse_where_clause(where_str)
            except ValueError as e:
                print(f"Ошибка парсинга: {e}")
                continue

            # Загружаем данные, обновляем и сохраняем
            table_data = load_table_data(table_name)
            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)

        elif command == "delete":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            table_name = args[1]

            # Проверяем существование таблицы
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            # Ищем WHERE в исходной строке команды
            if "WHERE" not in user_input.upper():
                print("Ошибка: отсутствует WHERE условие.")
                continue

            where_idx = user_input.upper().index("WHERE")
            where_str = user_input[where_idx + 5:].strip()

            try:
                where_clause = parse_where_clause(where_str)
            except ValueError as e:
                print(f"Ошибка парсинга WHERE: {e}")
                continue

            # Загружаем данные, удаляем и сохраняем
            table_data = load_table_data(table_name)
            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)

        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")