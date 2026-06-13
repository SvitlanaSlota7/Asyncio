import asyncio


# Функція для обробки конкретного клієнта
async def handle_client(reader, writer):
    # Отримуємо IP та порт клієнта
    client_address = writer.get_extra_info('peername')
    print(f"[НОВЕ ПІДКЛЮЧЕННЯ] Клієнт {client_address} підключився.")

    try:
        # Цикл для спілкування з цим клієнтом
        while True:
            # Асинхронно читаємо дані від клієнта (порціями до 1024 байт)
            data = await reader.read(1024)

            # Якщо дані порожні — клієнт відключився
            if not data:
                print(f"[ВІДКЛЮЧЕННЯ] Клієнт {client_address} розірвав з'єднання.")
                break

            # Декодуємо дані у текст
            message = data.decode('utf-8').strip()
            print(f"[{client_address}] Отримано: {message}")

            # Формуємо ехо-відповідь
            echo_message = f"Echo: {message}\n"

            # Відправляємо дані назад клієнту (кодуємо текст у байти)
            writer.write(echo_message.encode('utf-8'))
            # Чекаємо, поки дані фізично відправяться в мережу
            await writer.drain()

    except asyncio.CancelledError:
        print(f"[СИСТЕМНО] Задачу обробки клієнта {client_address} було скасовано.")
    except Exception as e:
        print(f"[ПОМИЛКА] Щось пішло не так з {client_address}: {e}")
    finally:
        # Закриваємо з'єднання з клієнтом
        print(f"[ЗАКРИТТЯ] Закриваємо сокет для {client_address}")
        writer.close()
        await writer.wait_closed()


# Функція запуску сервера
async def main():
    host = '127.0.0.1'  # Localhost
    port = 8888  # Порт для прослуховування

    # Запускаємо асинхронний сервер сокетів
    # На кожне нове підключення asyncio автоматично створює Task і викликає handle_client
    server = await asyncio.start_server(handle_client, host, port)

    # Отримуємо адреси, на яких сервер піднявся
    # (для start_server повертається список сокетів, беремо перший)
    server_address = server.sockets[0].getsockname()
    print(f"[СТАРТ] Ехо-сервер запущено на {server_address}")

    # Запускаємо нескінченне обслуговування запитів
    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[ЗУПИНКА] Сервер вимкнено користувачем.")