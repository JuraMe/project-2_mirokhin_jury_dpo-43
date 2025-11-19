import re

# Парсит строковое значение в правильный тип данных
def _parse_value(value_str):
    value_str = value_str.strip()

    # Проверяем, является ли значение строкой в кавычках
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        # Убираем кавычки и возвращаем строку
        return value_str[1:-1]

    # Проверяем на булевы значения
    if value_str.lower() in ('true', 'false'):
        return value_str.lower() == 'true'

    # Пытаемся преобразовать в int
    try:
        return int(value_str)
    except ValueError:
        pass

    # Если ничего не подошло, возвращаем как строку
    return value_str


