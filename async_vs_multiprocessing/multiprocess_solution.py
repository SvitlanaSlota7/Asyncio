import multiprocessing
import time
import math


# 1. Cинхронні функції для обчислень
def calc_fibonacci(n):
    if n <= 1:
        return n
    return calc_fibonacci(n - 1) + calc_fibonacci(n - 2)


def calc_factorial(n):
    return math.factorial(n)


def calc_square(n):
    return n ** 2


def calc_cubic(n):
    return n ** 3


if __name__ == "__main__":
    numbers = list(range(1, 11))

    start_time = time.perf_counter()

    # Gул процесів. Кількість процесів за замовчуванням дорівнює кількості ядер CPU
    with multiprocessing.Pool() as pool:
        # pool.map виконує функцію для кожного елемента зі списку паралельно
        fib_res = pool.map(calc_fibonacci, numbers)
        fact_res = pool.map(calc_factorial, numbers)
        sq_res = pool.map(calc_square, numbers)
        cube_res = pool.map(calc_cubic, numbers)

    end_time = time.perf_counter()

    print("МУЛЬТИПРОЦЕСОРНА РЕАЛІЗАЦІЯ ")
    print(f"Fibonacci: {fib_res}")
    print(f"Factorial: {fact_res}")
    print(f"Squares:   {sq_res}")
    print(f"Cubes:     {cube_res}")
    print(f"Час виконання: {end_time - start_time:.6f} секунд")