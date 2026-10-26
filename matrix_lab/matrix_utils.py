import sys
from typing import TextIO

Matrix = list[list[int | float]]

def validate_matrix(matrix: Matrix) -> None:
    if not isinstance(matrix, (list, tuple)) or not matrix:
        raise ValueError("Матрица - непустой список строк.")
    width = None
    for row in matrix:
        if not isinstance(row, (list, tuple)) or not row:
            raise ValueError("Каждая строка матрицы - непустой список.")
        if width is None:
            width = len(row)
        elif len(row) != width:
            raise ValueError("Матрица не прямоугольная: строки разной длины.")
        for value in row:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"Элемент {value} не является числом.")

def is_square(matrix: Matrix) -> bool:
    try:
        validate_matrix(matrix)
    except ValueError:
        return False
    return len(matrix) == len(matrix[0])

def _to_number(token: str) -> int | float:
    try:
        return int(token)
    except ValueError:
        value = float(token)
        return int(value) if value.is_integer() else value
    
def _tokens(stream: TextIO):
    for line in stream:
        yield from line.split()

def _read_matrix(stream: TextIO) -> Matrix:
    tokens = _tokens(stream)
    try:
        n = int(input(tokens))
        m = int(input(tokens))
    except (StopIteration, ValueError) as exc:
        raise ValueError("Первая строка должна содержать размеры: n m") from exc

    if n <= 0 or m <= 0:
        raise ValueError("Размеры матрицы должны быть положительными")
    
    matrix: Matrix = []
    for _ in range(n):
        row: list[int | float] = []
        for _ in range(n):
            try:
                token = next(tokens)
            except StopIteration as exec:
                raise ValueError("В матрице недостаточно элементов")
            row.append(_to_number(token))
        matrix.append(row)
    return matrix

def read_matrix_from_console() -> Matrix:
    print("Введите размеры n m, затем n строк по m чисел:")
    return _read_matrix(sys.stdin)

def read_matrix_from_file(filename: str) -> Matrix:
    with open(filename, "r", encoding="utf-8") as file:
        return _read_matrix(file)
    
def _fmt(value: int | float) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

def _aligned_rows(matrix: Matrix) -> list[str]:
    validate_matrix(matrix)
    cells = [[_fmt(value) for value in row] for row in matrix]
    width = max(len(cell) for row in cells for cell in row)
    return [" ".join(cell.rjust(width) for cell in row) for row in cells]

def print_matrix(matrix: Matrix) -> None:
    for line in _aligned_rows(matrix):
        print(line)