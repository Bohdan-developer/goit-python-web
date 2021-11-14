import socket
import threading
import time
from server import host, port


server = (host, port)  # Данные сервера


shutdown = False
join = False


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                print(data.decode("utf-8"))
                time.sleep(0.1)
        except:
            pass


# host = socket.gethostbyname(socket.gethostname())
# port = 0



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 0))
sock.setblocking(0)

nickname = input("Name :")

thread = threading.Thread(target=receving, args=("RecvThread", sock))
thread.start()


while shutdown == False:
    if nickname == False:
        sock.sendto((">>>" + nickname + " - " + "connect to chat").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            if message != "":
                sock.sendto(("[" + nickname + "] -> " + message).encode("utf-8"), server)
            time.sleep(0.1)
        except KeyboardInterrupt:
            sock.sendto((">>>" + nickname + " - " + " left chat").encode("utf-8"), server)
            shutdown = True

thread.join()
sock.close()
