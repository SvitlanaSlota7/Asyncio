import asyncio
import time
import math


# Асинхронні функції
async def calc_fibonacci(n):
    # Проста рекурсія для симуляції навантаження
    def fib(x):
        if x <= 1:
            return x
        return fib(x - 1) + fib(x - 2)

    # asyncio.sleep(0) дозволяє перемикати контекст
    await asyncio.sleep(0)
    return fib(n)


async def calc_factorial(n):
    await asyncio.sleep(0)
    return math.factorial(n)


async def calc_square(n):
    await asyncio.sleep(0)
    return n ** 2


async def calc_cubic(n):
    await asyncio.sleep(0)
    return n ** 3


# 2. Головна асинхронна функція
async def main():
    numbers = list(range(1, 11))  # Список від 1 до 10

    # Списки задач для кожної функції
    fib_tasks = [calc_fibonacci(n) for n in numbers]
    fact_tasks = [calc_factorial(n) for n in numbers]
    sq_tasks = [calc_square(n) for n in numbers]
    cube_tasks = [calc_cubic(n) for n in numbers]

    # Об'єднуємо всі таски в один список
    all_tasks = fib_tasks + fact_tasks + sq_tasks + cube_tasks

    start_time = time.perf_counter()

    # Виконуємо все паралельно за допомогою asyncio.gather
    results = await asyncio.gather(*all_tasks)

    end_time = time.perf_counter()

    # Розбиваємо загальний результат назад на 4 окремі списки
    # Оскільки numbers має довжину 10, кожна група займає 10 елементів
    fib_res = results[0:10]
    fact_res = results[10:20]
    sq_res = results[20:30]
    cube_res = results[30:40]

    print("АСИНХРОННА РЕАЛІЗАЦІЯ")
    print(f"Fibonacci: {fib_res}")
    print(f"Factorial: {fact_res}")
    print(f"Squares:   {sq_res}")
    print(f"Cubes:     {cube_res}")
    print(f"Час виконання: {end_time - start_time:.6f} секунд\n")


if __name__ == "__main__":
    asyncio.run(main())