import json
import uuid
from encodings.utf_8 import encode, decode

from defined import *
import database


def dekryptPassword(krypted:str) -> str:    # Без изменений
    return krypted


def isLogined(login, password) -> int:
    password = dekryptPassword(password)
    i = -1
    for key in database.users:
        i = i + 1
        value = database.users[key]
        if value[3] == login and value[4] == password:
            return i
    return -1


def isExists(login) -> bool:
    for key in database.users:
        value = database.users[key]
        if value[3] == login:
            return True
    return False


def send(data):
    return encode(json.dumps(data, ensure_ascii=True))[0]


def data0(data: SendData) -> bytes:
    return b"1" if isLogined(data[0], data[1]) != -1 else b"0"


def data1(data: SendData) -> bytes:
    if isLogined(data[0], data[1]) == -1:
        return b"0"
    result:list[User] = []
    for k in database.users:
        v = database.users[k]
        result.append(v[:-1])
    return send(result)


def data2(data: SendData) -> bytes:
    if isLogined(data[0], data[1]) == -1:
        return b"0"
    result:list[Task] = []
    for k in database.tasks:
        result.append(database.tasks[k])

    res = send(result)
    return res


def data3(data: SendData) -> bytes:
    if isExists(data[0]) or not data[3] in database.registerTokens:
        return b"0"
    database.registerTokens.remove(data[3])
    n = len(database.users)
    database.users[n] = (n, "Безымянный", 0, data[0], data[1])
    return b"1"


def data4(data: SendData) -> bytes:
    i = isLogined(data[0], data[1])
    if i == -1 or database.users[i][2] < 2:
        return b"0"
    generated = uuid.uuid4().__str__()
    while generated in database.registerTokens:
        generated = uuid.uuid4().__str__()
    database.registerTokens.append(generated)
    return encode(generated)[0]


def data5(data: SendData) -> bytes:
    i = isLogined(data[0], data[1])
    if i == -1:
        return b"0"

    return send(database.users[i][:-1])


def data6(data: SendData) -> bytes:
    i = isLogined(data[0], data[1])

    if i == -1 or database.users[i][2] == 0:
        return b"0"

    n = len(database.tasks)
    task = json.loads(data[3])
    task[0] = n
    database.tasks[n] = task
    return b"1"


def data7(data: SendData) -> bytes:
    i = isLogined(data[0], data[1])
    n = -1
    try:
        n = int(data[3])
    except: ...

    if i == -1 or n == -1:
        return b"0"

    key = ((i, n) if i < n else (n, i)).__str__()

    if key in database.chats.keys():
        return encodeData(database.chats[key])
    return encodeData([])


def data8(data: SendData) -> bytes:
    i = isLogined(data[0], data[1])

    if i == -1:
        return b"0"

    n, msg = json.loads(data[3])

    key = ((i, n) if i < n else (n, i)).__str__()

    if key in database.chats.keys():
        database.chats[key].append(msg)
    else:
        database.chats[key] = [msg]

    return b"1"


toParse = [data0, data1, data2, data3, data4, data5, data6, data7, data8]
