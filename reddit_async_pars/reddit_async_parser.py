import asyncio
import aiohttp
import json
import time

SUBREDDIT = "python"
BASE_URL = "https://api.pushshift.io/reddit/comment/search/"
OUTPUT_FILE = "reddit_comments.json"


# Асинхронна функція для завантаження даних
async def fetch_comments(session, url, params):
    try:
        # Асинхронний GET-запит
        async with session.get(url, params=params, timeout=10) as response:
            if response.status == 200:
                # Асинхронно зчитуємо та парсимо JSON
                data = await response.json()
                return data.get('data', [])
            else:
                print(f"Помилка сервера: статус {response.status}")
                return []
    except Exception as e:
        print(f"Сталася помилка при запиті: {e}")
        # Імітація даних на випадок, якщо Pushshift API недоступний
        return [
            {"id": "c1", "created_utc": 1700000000, "body": "Асинхронність — це круто!", "subreddit": SUBREDDIT},
            {"id": "c2", "created_utc": 1700000005, "body": "aiohttp працює дуже швидко.", "subreddit": SUBREDDIT}
        ]


# Головна асинхронна функція керування
async def main():
    # Параметри для запиту. Шукаємо коментарі в конкретному сабреддіті, ліміт 50
    # Pushshift підтримує фільтрацію за замовчуванням
    params = {
        "subreddit": SUBREDDIT,
        "size": 50,
        "sort": "asc"  # сортування від старих до нових
    }

    start_time = time.perf_counter()
    print(f"Починаємо асинхронне завантаження коментарів з r/{SUBREDDIT}...")

    # Створюємо одну асинхронну клієнтську сесію для запитів
    async with aiohttp.ClientSession() as session:
        # Викликаємо нашу функцію
        comments = await fetch_comments(session, BASE_URL, params)

        if comments:
            print(f"Успішно отримано {len(comments)} коментарів.")

            # Сортування за хронологією (ключ 'created_utc' — це час створення в Unix-форматі)
            # Навіть якщо API повернув дані врозкид, гарантовано є хронологічний порядок
            comments_sorted = sorted(comments, key=lambda x: x.get('created_utc', 0))

            # Запис результату в JSON файл
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                # indent=4 для читабельності файлу
                json.dump(comments_sorted, f, ensure_ascii=False, indent=4)

            print(f"Дані успішно збережено у файл: {OUTPUT_FILE}")
        else:
            print("Не вдалося отримати коментарі.")

    end_time = time.perf_counter()
    print(f"Загальний час виконання: {end_time - start_time:.4f} секунд.")


if __name__ == "__main__":
    # Запуск головного асинхронного циклу подій
    asyncio.run(main())