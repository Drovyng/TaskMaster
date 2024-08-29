import json
import socket, storage
import time

from defined import *
from encodings.utf_8 import encode, decode


def sendServer(data: bytes) -> bytes | None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.settimeout(5)
        client.connect((storage.serverIp, 25601))
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


def load(data: bytes):
    return json.loads(decode(data)[0])


def get_login() -> bool | None:
    data = sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        0,
        ""
    )))
    if data is None:
        return None
    return data == b"1"


def get_user() -> User:
    data = sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        5,
        ""
    )))
    if data is None or data == b"0":
        return None
    return load(data)


def get_userlist() -> list[User] | None:
    data = sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        1,
        ""
    )))
    if data is None or data == b"0":
        return None
    return load(data)


def get_tasklist() -> list[Task] | None:
    data = sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        2,
        ""
    )))
    if data is None or data == b"0":
        return None
    return load(data)


def send_newtask(task: Task):
    sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        6,
        json.dumps(task)
    )))


def get_chat(other: int) -> Chat | None:
    data = sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        7,
        f"{other}"
    )))

    if data is None or data == b"0":
        return None
    return load(data)


def send_chatmsg(other: int, message: str):
    sendServer(encodeData((
        storage.datas["login"],
        kryptPassword(storage.datas["password"]),
        8,
        json.dumps((other, message))
    )))
