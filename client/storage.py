import base64
import encodings.utf_8

from defined import *
from cryptography.fernet import Fernet

datas = {
    "login": "",
    "password": ""
}

def kryptPassword(normal:str) -> str:
    return normal


def dekryptPassword(krypted:str) -> str:
    return krypted


def save():
    global datas
    with open("localdata", "w") as file:
        json.dump(datas, file)
        file.close()


def load():
    global datas
    try:
        with open("localdata", "r") as file:
            data = json.load(file)
            data["password"] = dekryptPassword(datas["password"])
            datas = data
            file.close()
    except: ...


load()
