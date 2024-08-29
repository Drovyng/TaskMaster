import base64
import encodings.utf_8
import json

from cryptography.fernet import Fernet

datas = {
    "login": "",
    "password": ""
}
serverIp = ""

with open("serverIp") as file:
    serverIp = file.read()

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
            datas = data.copy()
            datas["password"] = dekryptPassword(data["password"])
            file.close()
    except: ...


load()
