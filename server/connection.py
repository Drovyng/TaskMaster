from defined import *
import database


def dekryptPassword(krypted:str) -> str:    # Без изменений
    return krypted


def isLogined(login, password) -> bool:
    password = dekryptPassword(password)
    print(login, password)
    for key in database.users:
        value = database.users[key]
        print(value[3], value[4])
        if value[3] == login and value[4] == password:
            return True
    return False


def data0(data: SendData) -> bytes:
    return b"1" if isLogined(data[0], data[1]) else b"0"


toParse = [data0]
