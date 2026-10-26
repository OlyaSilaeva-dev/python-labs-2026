from __future__ import annotations

import functools
import time
from typing import Callable

from matrix_lab import matrix_utils as utils

def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"Время выполнения: {elapsed:.6f} сек")
    return wrapper

def validate_square(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            raise ValueError("Функция ожидает матрицу первым аргументом")
        matrix = args[0]
        utils.validate_matrix(matrix)
        if not utils.is_square(matrix):
            raise ValueError(
                f"Ожидалась квадратная матрица, получена {len(matrix)}x{len(matrix[0])}"
            )
        return func(*args, **kwargs)
    return wrapper

