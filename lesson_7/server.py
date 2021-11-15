import socket
import time

host = socket.gethostbyname(socket.gethostname())
port = 8003

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

clients = list()
print(">>> Server Started")

flag_exit = False


while True:
    try:
        data, addr = sock.recvfrom(1024)

        if addr not in clients:
            print(addr)
            clients.append(addr)

        connection_time = time.strftime("%H:%M:%S %d-%m-%Y", time.localtime())

        print(">>> IP:" + addr[0] + " PORT:" + str(addr[1]) + " " + connection_time + " ", end="")
        print(data.decode("utf-8"))

        for client in clients:
            if addr != client:
                sock.sendto(data, client)

    except KeyboardInterrupt:
        print("\n >>> Server Stopped ")
        break


