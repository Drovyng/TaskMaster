from defined import *
import socket, select, connection

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 25601))
server.listen()

sockets_list = [server]


def parse_msg(unparsed: bytes) -> bytes:
    data = decodeData(unparsed)
    return connection.toParse[data[2]](data)


def receive_msg(client: socket.socket) -> bool | bytes:
    try:
        data = client.recv(65536)
        if not data:
            return False
        return parse_msg(data)
    except:
        return False

print("Сервер запущен!")

while True:
    rs, _, es = select.select(sockets_list, [], sockets_list)

    for sock in rs:
        if sock == server:
            client, addr = server.accept()
            try:
                data = client.recv(65536)

                if not data:
                    continue

                sockets_list.append(client)

                client.send(parse_msg(data))
            except:
                pass
        else:
            data = sock.recv(65536)

            if not data:
                sockets_list.remove(sock)
                continue

            try:
                sock.send(parse_msg(data))
            except:
                pass