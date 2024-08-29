import datetime
import encodings
import json

Task = (
    int,                # №
    str,                # Задача
    str,                # Описание
    str,                # Статус
    str,                # Сложность
    str,                # Срок
    list[int]           # Исполнители
)

User = (
    int,                # №
    str,                # Никнейм
    int,                # Роль
    str,                # Логин
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
    0,                  # Логин
    1,                  # Список Пользователей
    2,                  # Список Задач
    3,                  # Регистрация
    4,                  # Токен Регистрации Создать
    5,                  # Мой Аккаунт
    6,                  # Новая Задача
    7,                  # Получить Чат
    8,                  # Отправить сообщение
]
Chat = list[str]
ChatKey = (int, int)    # 2 айди пользователя
RoleTypes = [
    "Работник",
    "Заместитель",
    "Менеджер",
    "Директор"
]


def encodeData(data: SendData) -> bytes:
    return encodings.utf_8.encode(json.dumps(data, ensure_ascii=False))[0]


def decodeData(data: bytes) -> SendData:
    return json.loads(encodings.utf_8.decode(data)[0])
