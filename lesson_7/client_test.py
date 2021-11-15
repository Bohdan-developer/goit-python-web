import socket
import threading

server = (socket.gethostbyname(socket.gethostname()), 8000)  # Данные сервера
sor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sor.bind(('', 0)) # Задаем сокет как клиент

alias = input("Nickname ") # Вводим наш псевдоним
sor.sendto(("[" + alias + '] Connect to chatr').encode('utf-8'), server)# Уведомляем сервер о подключении




def read_sok():
    global flag_close
    while flag_close:
        try:
            data = sor.recvfrom(1024)
            print(data.decode('utf-8'))
        except :
            flag_close = False
            sor.close()


if __name__ == '__main__':
    flag_close = True
    potok = threading.Thread(target= read_sok)
    potok.start()
    while flag_close:
        try:
            mensahe = input()
            sor.sendto(('[' + alias + '] ' + mensahe).encode('utf-8'), server)
        except KeyboardInterrupt:
            sor.sendto(('[' + alias + '] left chat').encode('utf-8'), server)
            flag_close = False
            sor.close()

    potok.join()

