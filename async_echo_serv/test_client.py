import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888))

# Відправляємо повідомлення
client.sendall(b"Hello, Async Server!\n")

# Отримуємо відповідь
response = client.recv(1024)
print("Відповідь сервера:", response.decode('utf-8'))

client.close()