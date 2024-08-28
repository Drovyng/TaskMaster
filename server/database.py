import json
import os

from defined import *

tasks: dict[int, Task] = {

}
users: dict[int, UserDatabase] = {
    0: (0, "Лох", "Менеджер", "loh", "12345")
}


def saveSingle(name, data):
    name = name + ".json"
    with open(name, "w") as file:
        return json.dump(data, file, ensure_ascii=False)


def loadSingle(name, default) -> dict:
    name = name + ".json"
    if os.path.exists(name):
        with open(name, "r") as file:
            return json.load(file)
    return default


def save():
    global tasks, users
    saveSingle("tasks", tasks)
    saveSingle("users", users)


def load():
    global tasks, users
    tasks = loadSingle("tasks", tasks)
    users = loadSingle("users", users)


load()