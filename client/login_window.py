from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtGui import QFont
import storage


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.resize(300, 150)

        self.login_action = None
        self.logined_action = None

        # Элементы формы
        self.login_label = QLabel("Логин:")
        self.login_label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.login_input = QLineEdit()
        self.login_input.setAlignment(Qt.AlignCenter)
        self.password_label = QLabel("Пароль:")
        self.password_label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрыть пароль
        self.password_input.setAlignment(Qt.AlignCenter)
        self.login_button = QPushButton("Отправить")
        self.login_button.clicked.connect(self.login)
        self.status_label = QLabel(" ")
        self.status_label.setAlignment(Qt.AlignCenter)  # Центрируем текст

        # Настраиваем шрифт для всех меток
        font = QFont()
        font.setPointSize(14)  # Увеличиваем размер шрифта
        self.login_label.setFont(font)
        self.password_label.setFont(font)
        self.password_label.setFont(font)
        self.login_input.setFont(font)
        self.password_input.setFont(font)
        self.login_button.setFont(font)
        font2 = QFont()
        font2.setPointSize(11)
        self.status_label.setFont(font2)

        # Расположение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.status_label)
        layout.addLayout(hbox)

        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def autologin(self, login: str, password: str):
        if len(login) > 0 and len(password) > 0:
            self.login_input.setText(login)
            self.password_input.setText(password)

    def login(self):
        self.status_label.setStyleSheet("")
        # Делаем поля неактивными
        self.login_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.login_button.setEnabled(False)

        storage.datas["login"] = self.login_input.text()
        storage.datas["password"] = self.password_input.text()

        # Отображаем строку состояния
        self.status_label.setText("подключение...")

        QApplication.processEvents()

        if not self.login_action is None:
            yes = self.login_action()
            if yes is None:
                self.status_label.setText("нет соединения с сервером")
            elif not yes:
                self.status_label.setText("неправильный логин или пароль")
            self.status_label.setStyleSheet("color: " + ("green" if yes else "red") + ";")
            QApplication.processEvents()
            if yes:
                storage.save()
                self.logined_action()
                self.close()
                QApplication.processEvents()
            else:
                self.login_input.setEnabled(True)
                self.password_input.setEnabled(True)
                self.login_button.setEnabled(True)
                QApplication.processEvents()