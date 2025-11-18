import json
import os
from primitive_db.constants import DATA_DIR, ENCODING

# Загружает данные из JSON-файла
def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Сохраняет переданные данные в JSON-файл
def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Создает директорию для данных если её нет
def ensure_data_dir():
    """Создает директорию для данных таблиц если она не существует"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)