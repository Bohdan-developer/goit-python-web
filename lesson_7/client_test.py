import socket
import threading

server = ('192.168.1.110', 8003)  # Данные сервера
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sor.bind(('', 0)) # Задаем сокет как клиент

alias = input("Nickname ") # Вводим наш псевдоним
sor.sendto(("[" + alias + '] Connect to chatr').encode('utf-8'), server)# Уведомляем сервер о подключении

flag_close = False

def read_sok():
    while True:
        data = sor.recvfrom(1024)
        print(data.decode('utf-8'))


if __name__ == '__main__':
    potok = threading.Thread(target= read_sok)
    potok.start()
    while True:
        try:
            mensahe = input()
            sor.sendto(('[' + alias + '] ' + mensahe).encode('utf-8'), server)
        except KeyboardInterrupt:
            sor.sendto(('[' + alias + '] left chat').encode('utf-8'), server)
            sor.close()

    potok.join()

