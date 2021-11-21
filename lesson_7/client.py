import socket
import threading

server = (socket.gethostbyname(socket.gethostname()), 8000)
flag_close = True


def client_receives_msg():
    global flag_close
    while flag_close:
        try:
            data = soc.recv(1024)
            print(data.decode('utf-8'))
        except:
            flag_close = False


with socket.socket() as soc:
    soc.bind(("", 0))
    soc.connect(server)
    alias = input("Nickname ")  # Вводим наш псевдоним
    soc.sendto(("[" + alias + '] Connect to chat').encode('utf-8'), server)  # Уведомляем сервер о подключении
    potok = threading.Thread(target=client_receives_msg)
    potok.start()

    while flag_close:
        try:
            message = input("Message: ")
            soc.sendto(("[" + alias + '] ' + message).encode('utf-8'), server)
        except KeyboardInterrupt:
            soc.sendto(('[' + alias + '] left chat').encode('utf-8'), server)
            flag_close = False

    potok.join()




