import socket, storage
import time

from defined import *


def sendServer(data: bytes) -> bytes | None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.settimeout(5)
        client.connect(("localhost", 25601))
        client.send(data)
        data = client.recv(65536)
        client.close()
        return data
    except:
        try:
            client.close()
        except:
            return None
        return None



def kryptPassword(normal:str) -> str:       # Без изменений
    return normal


def get_login() -> bool | None:
    data = sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        0,
        ""
    )))
    print(data)
    if data is None:
        return None
    return data == b"1"
