import datetime
import encodings
import json

Task = (
    int,                # №
    str,                # Название
    str,                # Описание
    str,                # Статус
    int,                # Сложность
    datetime.datetime,  # Срок
    list[int]           # Назначенные
)

User = (
    int,                # №
    str,                # Никнейм
    int                 # Роль
)
UserDatabase = (
    int,                # №
    str,                # Никнейм
    int,                # Роль
    str,                # Логин
    str                 # Пароль
)
SendData = (
    str,                # Логин
    str,                # Пароль
    int,                # Тип Отправки
    str                 # Данные в Json
)
SendDataTypes = [
    0,          # Логин
    1,          # Список Пользователей
    2,          # Список Задач
]
def encodeData(data: SendData) -> bytes:
    return encodings.utf_8.encode(json.dumps(data, ensure_ascii=False))[0]


def decodeData(data: bytes) -> SendData:
    return json.loads(encodings.utf_8.decode(data)[0])