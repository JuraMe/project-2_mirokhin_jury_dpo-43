import functools
import time
from typing import Callable


def confirm_action(action_name: str):
    """
    Декоратор-фабрика для запроса подтверждения опасных операций.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Запрашиваем подтверждение у пользователя
            prompt = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            response = input(prompt)

            # Если пользователь подтвердил действие
            if response.lower() == 'y':
                return func(*args, **kwargs)
            else:
                print(f"Операция '{action_name}' отменена.")
                return args[0] if args else None  # Возвращаем metadata без изменений

        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    """
    Декоратор для замера времени выполнения функции.
    Выводит в консоль время выполнения в секундах.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed_time:.3f} секунд")
        return result

    return wrapper


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