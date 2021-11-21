import socket
import time

host = socket.gethostbyname(socket.gethostname())
port = 8000
print(host)

clients = list()


with socket.socket() as sock:
    sock.bind((host, port))
    sock.listen(10)
    print("Started Server")
    while True:
        conn, addr = sock.accept()
        print(f'Connection {addr}')

        if addr not in clients:
            clients.append(addr)
        connection_time = time.strftime("%H:%M:%S %d-%m-%Y", time.localtime())

        while True:
            try:
                request = conn.recv(1024)
                if not request:
                    break
                # print(request.decode())
                # conn.sendall(b"Ok is connect!")

                print(">>> IP:" + addr[0] + " PORT:" + str(addr[1]) + " " + connection_time + " ", end="")
                print(request.decode("utf-8"))
                sock.sendto(b"Ok conected", addr)

                for client in clients:
                    if addr != client:
                        try:
                            sock.send(request, client)
                        except:
                            print(" error send")

            except KeyboardInterrupt:
                print("Stooped sever")
