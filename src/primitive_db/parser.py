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

# Парсит WHERE условие в словарь
def parse_where_clause(where_str):

    """
    Парсит WHERE условие вида "age = 28 AND name = 'John'"
    в словарь {'age': 28, 'name': 'John'}

    Поддерживает:
    - Несколько условий через AND
    - Строковые значения в одинарных или двойных кавычках
    - Числовые значения (int)
    - Булевы значения (true/false)

    Примеры:
    - "ID = 1" -> {'ID': 1}
    - "name = 'John'" -> {'name': 'John'}
    - "age = 28 AND active = true" -> {'age': 28, 'active': True}
    """
    if not where_str or not where_str.strip():
        return {}

    result = {}

    # Разделяем по AND (case-insensitive)
    conditions = re.split(r'\s+AND\s+', where_str.strip(), flags=re.IGNORECASE)

    for condition in conditions:
        condition = condition.strip()

        # Ищем знак равенства
        if '=' not in condition:
            raise ValueError(f"Некорректное условие: {condition}. Ожидается формат 'поле = значение'")

        # Разделяем по знаку равенства
        parts = condition.split('=', 1)
        if len(parts) != 2:
            raise ValueError(f"Некорректное условие: {condition}")

        key = parts[0].strip()
        value_str = parts[1].strip()

        # Парсим значение
        value = _parse_value(value_str)
        result[key] = value

    return result
