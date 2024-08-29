import encodings.utf_8
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, Qt, QTimer, QDateTime, QModelIndex
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QBoxLayout, QAbstractItemView, QDateTimeEdit, QListWidget, QListWidgetItem, QCheckBox,
)

import login_window
import storage, connection
from defined import *


class AddTaskWindow(QWidget):
    def __init__(self, users:list[User]):
        super().__init__()
        self.setWindowTitle("Добавить Задачу")
        self.resize(300, 150)

        # Элементы формы
        self.taskL = QLabel("Задача:")
        self.taskL.setAlignment(Qt.AlignCenter)
        self.task = QLineEdit()
        self.task.setAlignment(Qt.AlignCenter)

        self.descL = QLabel("Описание:")
        self.descL.setAlignment(Qt.AlignCenter)
        self.desc = QLineEdit()
        self.desc.setAlignment(Qt.AlignCenter)

        self.dateL = QLabel("Срок:")
        self.dateL.setAlignment(Qt.AlignCenter)
        self.date = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.date.setDisplayFormat("HH:mm  dd.MM.yyyy")
        self.date.setAlignment(Qt.AlignCenter)

        self.statusL = QLabel("Статус:")
        self.statusL.setAlignment(Qt.AlignCenter)
        self.status = QLineEdit()
        self.status.setAlignment(Qt.AlignCenter)

        self.diffL = QLabel("Сложность:")
        self.diffL.setAlignment(Qt.AlignCenter)
        self.diff = QLineEdit()
        self.diff.setAlignment(Qt.AlignCenter)

        self.usersL = QLabel("Исполнители:")
        self.usersL.setAlignment(Qt.AlignCenter)
        self.users = QListWidget(self)
        self.users.setSelectionMode(QListWidget.ExtendedSelection)
        self.users.setFixedHeight(75)

        for user in users:
            list_item = QListWidgetItem(f"{user[1]} (@{user[3]})")
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
            list_item.setCheckState(Qt.Unchecked)
            self.users.addItem(list_item)

        self.send_btn = QPushButton("Отправить")
        self.send_btn.clicked.connect(self.send)

        # Настраиваем шрифт для всех меток
        font = QFont()
        font.setPointSize(12)  # Увеличиваем размер шрифта

        self.taskL.setFont(font)
        self.task.setFont(font)

        self.descL.setFont(font)
        self.desc.setFont(font)

        self.dateL.setFont(font)
        self.date.setFont(font)

        self.statusL.setFont(font)
        self.status.setFont(font)

        self.diffL.setFont(font)
        self.diff.setFont(font)

        self.usersL.setFont(font)
        self.users.setFont(font)

        self.send_btn.setFont(font)

        # Расположение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.taskL)
        layout.addWidget(self.task)
        layout.addWidget(self.descL)
        layout.addWidget(self.desc)
        layout.addWidget(self.dateL)
        layout.addWidget(self.date)
        layout.addWidget(self.statusL)
        layout.addWidget(self.status)
        layout.addWidget(self.diffL)
        layout.addWidget(self.diff)
        layout.addWidget(self.usersL)
        layout.addWidget(self.users)
        layout.addWidget(self.send_btn)
        self.setLayout(layout)

    def send(self):
        connection.send_newtask((
            0,
            self.task.text(),
            self.desc.text(),
            self.status.text(),
            self.diff.text(),
            self.date.text(),
            [i for i in range(self.users.count()) if self.users.item(i).checkState() == Qt.Checked]
        ))
        self.close()


class TaskMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Task Master"
        self.setWindowTitle(self.title)
        # self.setWindowIcon(QIcon("task_icon.png"))
        self.width, self.height = 1280, 720
        self.resize(self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.user:User = None
        self.noConnection = False

        self.tableTasksIndices:list[int] = []
        self.tableTasks:list[Task] = []
        self.users:list[User] = []
        self.usersIndices:list[int] = []

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Задача", "Срок", "Статус", "Сложность"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setFixedSize(400, self.height-50)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setDefaultSectionSize(97)
        self.table.horizontalHeader().setSectionsClickable(False)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAutoScroll(False)
        self.table.cellClicked.connect(self.selectTask)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.empty = QWidget()
        self.empty.setFixedHeight(self.height - 280)

        self.view_task = QTableWidget(7, 1)
        self.view_task.horizontalHeader().setVisible(False)
        self.view_task.setVerticalHeaderLabels(["№", "Задача", "Описание", "Статус", "Сложность", "Срок", "Исполнители"])
        self.view_task.verticalHeader().setSectionsClickable(False)
        self.view_task.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.view_task.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.view_task.setFixedHeight(280)
        self.view_task.verticalHeader().setMinimumSectionSize(40)
        self.view_task.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.view_task.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.view_task.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_task.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_task.verticalHeader().setStretchLastSection(True)
        self.view_task.setAutoScroll(False)
        self.view_task.setEditTriggers(QTableWidget.NoEditTriggers)
        self.view_task.horizontalHeader().setDefaultSectionSize(1280)

        self.view_chat = QListWidget()
        self.view_chat.setFixedHeight(280)
        self.view_chat.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

        ifont = QFont()
        ifont.setPointSize(14)

        self.view_chat_input = QLineEdit()
        self.view_chat_input.setFont(ifont)
        self.view_chat_send = QPushButton("➤")
        self.view_chat_send.setFixedWidth(50)
        self.view_chat_send.setFont(ifont)
        self.view_chat_send.clicked.connect(self.sendMessage)

        self.chats = QTableWidget(0, 1)
        self.chats.setSelectionMode(QListWidget.SingleSelection)
        self.chats.horizontalHeader().setVisible(False)
        self.chats.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chats.horizontalHeader().setDefaultSectionSize(200)
        self.chats.setEditTriggers(QTableWidget.NoEditTriggers)
        self.chats.verticalHeader().setVisible(False)
        self.chats.setFixedWidth(200)
        self.chats.cellClicked.connect(self.selectChat)


        # Таймер для обновления статуса
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reload)
        self.timer.start(30000)  # Обновление каждые 30 секунд

        font = QFont()
        font.setPointSize(10)

        # Кнопки
        self.table_add = QPushButton("Добавить")
        self.table_add.clicked.connect(self.addTask)
        self.table_edit = QPushButton("Менеджер")
        self.table_edit.clicked.connect(self.editTasks)
        self.table_edit.setDisabled(True)
        self.table_every = QCheckBox()
        self.table_every.setText("Показать всё")
        self.table_every.clicked.connect(self.loadTasks)
        self.table_every.setFont(font)

        self.load()

        # Расположение элементов
        layout0 = QBoxLayout(QBoxLayout.Direction.LeftToRight)

        layout2 = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout2.addWidget(self.table_every)
        if self.user[2] > 0:
            layout2.addWidget(self.table_add)
            layout2.addWidget(self.table_edit)

        layout1 = QVBoxLayout()
        layout1.addWidget(self.table)
        layout1.addLayout(layout2)

        layout4 = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout4.addWidget(self.view_chat_input)
        layout4.addWidget(self.view_chat_send)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.empty)
        layout3.addWidget(self.view_task)
        layout3.addWidget(self.view_chat)
        layout3.addLayout(layout4)

        layout0.addWidget(self.chats)
        layout0.addLayout(layout3)
        layout0.addLayout(layout1)
        self.setLayout(layout0)

        self.view_chat.setVisible(False)
        self.view_task.setVisible(False)
        self.view_chat_input.setVisible(False)
        self.view_chat_send.setVisible(False)

        self.selectChat()

    def selectTask(self):
        self.view_chat.setVisible(False)
        self.view_chat_input.setVisible(False)
        self.view_chat_send.setVisible(False)
        self.view_task.setVisible(True)
        task = self.tableTasks[self.tableTasksIndices[self.table.currentRow()]]

        self.view_task.setItem(0, 0, QTableWidgetItem(f"{task[0]}"))
        self.view_task.setItem(1, 0, QTableWidgetItem(f"{task[1]}"))
        self.view_task.setItem(2, 0, QTableWidgetItem(f"{task[2]}"))
        self.view_task.setItem(3, 0, QTableWidgetItem(f"{task[3]}"))
        self.view_task.setItem(4, 0, QTableWidgetItem(f"{task[4]}"))
        self.view_task.setItem(5, 0, QTableWidgetItem(f"{task[5]}"))

        humans = ""
        if len(task[6]) > 0:
            for i in task[6]:
                humans = humans + ", " + f"{self.users[i][1]} (@{self.users[i][3]})"
            humans = humans.removeprefix(", ")
        else:
            humans = "Нет исполнителей."
        self.view_task.setItem(6, 0, QTableWidgetItem(humans))


    def selectChat(self):
        font = QFont()
        font.setPointSize(20)
        self.view_task.setVisible(False)
        self.view_chat.setVisible(True)
        self.view_chat_input.setVisible(True)
        self.view_chat_send.setVisible(True)
        user = self.usersIndices[self.chats.currentRow()]
        chat = connection.get_chat(user)

        self.view_chat.clear()
        for msg in chat:
            isMe = msg[0] == ">"
            item = QListWidgetItem(msg[1:])
            if self.user[0] < user:
                isMe = not isMe
            item.setTextAlignment(Qt.AlignRight if isMe else Qt.AlignLeft)
            item.setFont(font)
            self.view_chat.addItem(item)

        self.view_chat_input.setText("")

    def sendMessage(self):
        if len(self.view_chat_input.text()) > 0:
            n = self.usersIndices[self.chats.currentRow()]
            sendChar = ">" if self.user[0] > n else "<"
            connection.send_chatmsg(n, sendChar + self.view_chat_input.text())
        self.view_chat_input.setText("")
        self.selectChat()

    def addTask(self):
        self.taskWin = AddTaskWindow(self.users)
        self.taskWin.update()
        QApplication.processEvents()
        self.taskWin.show()

    def editTasks(self):
        self.taskWin = AddTaskWindow(self.users)
        self.taskWin.update()
        QApplication.processEvents()
        self.taskWin.show()

    def reload(self):
        self.load()
        if self.view_task.isVisible():
            self.selectTask()
        else:
            self.selectChat()

    def load(self):
        self.user = connection.get_user()
        self.loadTasks()
        self.users = connection.get_userlist()
        self.usersIndices = []
        self.chats.setRowCount(0)
        self.chatsIndices = []
        i = -1
        for user in self.users:
            i = i + 1
            if user[0] == self.user[0]:
                continue
            self.usersIndices.append(i)
            row = self.chats.rowCount()
            self.chats.insertRow(row)
            item = QTableWidgetItem(f"{user[1]} (@{user[3]})")
            item.font().setPointSize(14)
            self.chats.setItem(row, 0, item)

    def coloredTaskCell(self, text:str, isMine:bool) -> QTableWidgetItem:
        ret = QTableWidgetItem(text)
        if not isMine:
            ret.setBackground(QBrush(QColor(200, 200, 200)))
        return ret

    def loadTasks(self):
        self.table.setRowCount(0)
        self.tableTasks = []
        self.tableTasksIndices = []
        every = self.table_every.checkState() == Qt.Checked
        i = -1
        for task in connection.get_tasklist():
            i = i + 1
            yes = self.user[0] in task[6]
            if every or yes:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.tableTasks.append(task)
                self.tableTasksIndices.append(i)

                self.table.setItem(row, 0, self.coloredTaskCell(task[1], yes))
                self.table.setItem(row, 1, self.coloredTaskCell(task[5], yes))
                self.table.setItem(row, 2, self.coloredTaskCell(task[3], yes))
                self.table.setItem(row, 3, self.coloredTaskCell(task[4], yes))



app = QApplication(sys.argv)

login_win = login_window.LoginWindow()


def login():
    return connection.get_login()

launchMain = False

def login_success():
    global launchMain
    launchMain = True


login_win.login_action = login
login_win.logined_action = login_success

login_win.autologin(storage.datas["login"], storage.datas["password"])
login_win.show()


app.exec_()

if launchMain:
    win = TaskMaster()
    win.show()

    app.exec_()