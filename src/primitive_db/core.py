from primitive_db.constants import VALID_TYPES
from primitive_db.utils import load_table_data, save_table_data, create_cacher
from primitive_db.decorators import handle_db_errors, confirm_action, log_time

# Создаем глобальный кэшер для функции select
_select_cache = create_cacher()


# Создание таблицы с указанными столбцами
@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_structure = {"ID": "int"}

    for col in columns:
        name, col_type = col.split(":")
        if col_type not in VALID_TYPES:
            print(f"Некорректный тип данных: {col_type}. Попробуйте снова.")
            return metadata
        table_structure[name] = col_type

    metadata[table_name] = table_structure
    print(f'Таблица "{table_name}" успешно создана со столбцами: '
          f'{", ".join([f"{k}:{v}" for k, v in table_structure.items()])}')
    return metadata

# Удаление таблицы
@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

# Валидация и преобразование значения в соответствии с типом
def _validate_and_convert(value, expected_type):
    if expected_type == "int":
        try:
            return int(value)
        except ValueError:
            return None
    elif expected_type == "str":
        return str(value)
    elif expected_type == "bool":
        if value.lower() in ("true", "1", "yes"):
            return True
        elif value.lower() in ("false", "0", "no"):
            return False
        else:
            return None
    return None

# Добавление новой записи в таблицу
@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    # Проверка существования таблицы
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    # Получаем схему таблицы
    schema = metadata[table_name]
    # Убираем ID из схемы для проверки количества столбцов
    columns = {k: v for k, v in schema.items() if k != "ID"}

    # Проверка количества переданных значений
    if len(values) != len(columns):
        print(f"Ошибка: Ожидается {len(columns)} значений, получено {len(values)}.")
        print(f"Столбцы: {', '.join(columns.keys())}")
        return

    # Валидация типов данных
    record = {}
    for (col_name, col_type), value in zip(columns.items(), values):
        converted_value = _validate_and_convert(value, col_type)
        if converted_value is None and col_type != "str":
            print(
                f"Ошибка: Некорректное значение '{value}' "
                f"для столбца '{col_name}' типа '{col_type}'."
            )
            return
        record[col_name] = converted_value

    # Загружаем текущие данные таблицы
    table_data = load_table_data(table_name)

    # Генерируем новый ID
    new_id = table_data["next_id"]
    record["ID"] = new_id

    # Добавляем запись
    table_data["records"].append(record)
    table_data["next_id"] += 1

    # Сохраняем обновленные данные
    save_table_data(table_name, table_data)

    print(f'Запись успешно добавлена в таблицу "{table_name}" с ID={new_id}.')
    return table_data

# Выборка записей из таблицы с опциональной фильтрацией
@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    import json

    # Создаем уникальный ключ для кэша на основе данных и условия
    # Используем JSON сериализацию для создания уникального ключа
    cache_key = json.dumps({
        "records_hash": hash(json.dumps(table_data.get("records", []), sort_keys=True)),
        "where_clause": where_clause
    }, sort_keys=True)

    # Определяем функцию для получения результата (вызывается только при промахе кэша)
    def compute_result():
        records = table_data.get("records", [])

        # Если фильтр не задан, возвращаем все записи
        if where_clause is None:
            return records

        # Фильтруем записи по условию where_clause
        filtered_records = []
        for record in records:
            match = True
            for key, value in where_clause.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                filtered_records.append(record)

        return filtered_records

    # Используем кэширование
    return _select_cache(cache_key, compute_result)

# Обновление записей в таблице
@handle_db_errors
def update(table_data, set_clause, where_clause):
    records = table_data.get("records", [])
    updated_count = 0

    # Проходим по всем записям
    for record in records:
        # Проверяем, соответствует ли запись условию where_clause
        match = True
        for key, value in where_clause.items():
            if key not in record or record[key] != value:
                match = False
                break

        # Если запись соответствует условию, обновляем её
        if match:
            for key, value in set_clause.items():
                if key in record:
                    record[key] = value
            updated_count += 1

    print(f"Обновлено записей: {updated_count}")
    return table_data

# Удаление записей из таблицы
@confirm_action("удаление записей")
@handle_db_errors
def delete(table_data, where_clause):
    records = table_data.get("records", [])
    records_to_keep = []
    deleted_count = 0

    # Проходим по всем записям
    for record in records:
        # Проверяем, соответствует ли запись условию where_clause
        match = True
        for key, value in where_clause.items():
            if key not in record or record[key] != value:
                match = False
                break

        # Если запись НЕ соответствует условию, оставляем её
        if not match:
            records_to_keep.append(record)
        else:
            deleted_count += 1

    # Обновляем список записей
    table_data["records"] = records_to_keep

    print(f"Удалено записей: {deleted_count}")
    return table_data


# Функции для управления кэшем select
def clear_select_cache():
    """Очистить кэш для операций select"""
    _select_cache.clear()


def get_select_cache_stats():
    """Получить статистику кэша select"""
    return _select_cache.stats()