from primitive_db.constants import VALID_TYPES

# Создание таблицы с указанными столбцами
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_structure = {"ID": "int"}

    for col in columns:
        try:
            name, col_type = col.split(":")
            if col_type not in VALID_TYPES:
                print(f"Некорректный тип данных: {col_type}. Попробуйте снова.")
                return metadata
            table_structure[name] = col_type
        except ValueError:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

    metadata[table_name] = table_structure
    print(f'Таблица "{table_name}" успешно создана со столбцами: '
          f'{", ".join([f"{k}:{v}" for k, v in table_structure.items()])}')
    return metadata

# Удаление таблицы
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata