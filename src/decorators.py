import functools
from typing import Callable


def handle_db_errors(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок при работе с базой данных.
    Оборачивает вызов функции в блок try...except и обрабатывает исключения.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Ошибка: Файл не найден - {e}")
        except KeyError as e:
            print(f"Ошибка: Таблица, столбец или ключ не найден - {e}")
        except ValueError as e:
            print(f"Ошибка: Некорректное значение - {e}")
        except TypeError as e:
            print(f"Ошибка: Неверный тип данных - {e}")
        except PermissionError as e:
            print(f"Ошибка: Недостаточно прав доступа - {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при выполнении {func.__name__}: {e}")
        return None

    return wrapper