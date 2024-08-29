import json
import os
import threading

from defined import *

tasks: dict[int, Task] = {
    0: (0, "Ничего не делать", "необходимое занятие", "поиск работников", "очень легко", "13:37 31.08.2024", [1])
}
users: dict[int, UserDatabase] = {
    0: (0, "Главный", 3, "admin", "admin"),
    1: (1, "Тестер-работник", 0, "tester", "12345")
}
registerTokens:list[str] = [

]
chats: dict[str, Chat] = {

}

def saveSingle(name, data):
    if not os.path.exists("database"):
        os.mkdir("database")
    name = "database/" + name + ".json"
    with open(name, "w") as file:
        return json.dump(data, file, ensure_ascii=False)


def loadSingle(name, default) -> dict:
    name = "database/" + name + ".json"
    if os.path.exists(name):
        with open(name, "r") as file:
            return json.load(file)
    return default


def save():
    global tasks, users
    saveSingle("tasks", tasks)
    saveSingle("users", users)
    saveSingle("registerTokens", registerTokens)
    saveSingle("chats", chats)


def load():
    global tasks, users, registerTokens, chats
    tasks = loadSingle("tasks", tasks)
    users = loadSingle("users", users)
    registerTokens = loadSingle("registerTokens", registerTokens)
    chats = loadSingle("chats", chats)


load()
