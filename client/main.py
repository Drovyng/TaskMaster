import encodings.utf_8
import sys

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
)

import login_window
import storage, connection

class TaskMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Master")
        # self.setWindowIcon(QIcon("task_icon.png"))  # Замените "task_icon.png" на иконку
        self.resize(600, 400)

        # Настройки таблицы задач
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Задача", "Статус", "Срок"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Поля ввода данных
        self.task_label = QLabel("Задача:")
        self.task_input = QLineEdit()
        self.status_label = QLabel("Статус:")
        self.status_input = QLineEdit("Новая")
        self.deadline_label = QLabel("Срок:")
        self.deadline_input = QLineEdit()

        # Кнопки
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_task)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_task)

        # Расположение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.task_label)
        layout.addWidget(self.task_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_task(self):
        task = self.task_input.text()
        status = self.status_input.text()
        deadline = self.deadline_input.text()

        encodings.utf_8.encode()
        if not task:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите задачу.")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(task))
        self.table.setItem(row, 1, QTableWidgetItem(status))
        self.table.setItem(row, 2, QTableWidgetItem(deadline))

        self.task_input.clear()
        self.status_input.setText("Новая")
        self.deadline_input.clear()

    def delete_task(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)


app = QApplication(sys.argv)
print(storage.datas)
login_win = login_window.LoginWindow(storage.datas["login"], storage.datas["password"])


def login():
    return connection.get_login()


def login_success():
    task_master = TaskMaster()
    task_master.show()


login_win.login_action = login
login_win.logined_action = login_success


login_win.show()
sys.exit(app.exec_())
