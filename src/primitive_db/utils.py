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