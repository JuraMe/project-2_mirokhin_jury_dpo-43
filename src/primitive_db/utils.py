import json
import os

from primitive_db.constants import DATA_DIR, ENCODING
from primitive_db.decorators import handle_db_errors


# Загружает данные из JSON-файла
def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Сохраняет переданные данные в JSON-файл
@handle_db_errors
def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Создает директорию для данных если её нет
@handle_db_errors
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# Получает путь к файлу данных таблицы
def get_table_data_path(table_name):
    return os.path.join(DATA_DIR, f"{table_name}.json")

# Загружает данные таблицы
def load_table_data(table_name):
    ensure_data_dir()
    filepath = get_table_data_path(table_name)
    try:
        with open(filepath, "r", encoding=ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return {"next_id": 1, "records": []}

# Сохраняет данные таблицы
@handle_db_errors
def save_table_data(table_name, data):
    ensure_data_dir()
    filepath = get_table_data_path(table_name)
    with open(filepath, "w", encoding=ENCODING) as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Функция с замыканием для кэширования результатов
def create_cacher():
    """
    Создает функцию кэширования с замыканием.
    """
    # Кэш хранится в замыкании
    cache = {}

    def cache_result(key, value_func):
        """
        Функция для кэширования результатов.
        """
        # Проверяем, есть ли результат в кэше
        if key in cache:
            print(f"[CACHE HIT] Возвращен кэшированный результат для ключа: {key}")
            return cache[key]

        # Если результата нет, вызываем функцию для получения данных
        print(f"[CACHE MISS] Вычисление результата для ключа: {key}")
        result = value_func()

        # Сохраняем результат в кэш
        cache[key] = result

        return result

    # Добавляем методы для управления кэшем
    def clear_cache():
        """Очистить весь кэш"""
        cache.clear()
        print("[CACHE] Кэш очищен")

    def get_cache_stats():
        """Получить статистику кэша"""
        return {
            "size": len(cache),
            "keys": list(cache.keys())
        }

    # Добавляем дополнительные методы к функции
    cache_result.clear = clear_cache
    cache_result.stats = get_cache_stats

    return cache_result