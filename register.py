import sys
import sqlite3

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


DB_NAME = 'server_db.sqlite'


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(550, 550)

        # Подключение дизайна
        uic.loadUi('design/registration.ui', self)
        self.setWindowTitle('Вход в почту')
        self.label_2.resize(135, 22)
        self.label_3.setText('')
        self.label_3.resize(160, 41)
        self.lineEdit.setMaxLength(15)

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)

        # Подключение базы данных
        self.db = sqlite3.connect(DB_NAME)
        self.cur = self.db.cursor()

    def login(self):
        try:
            username = self.lineEdit.text()
            # Проверка, есть ли пользователь в базе
            if self.cur.execute(f"SELECT name FROM users WHERE name = '{username}'").fetchone() is None:
                self.label_3.setText('Пользователь не найден')
            else:
                self.label_3.setText('Успешный вход')
        except Exception as e:
            self.label_3.setText('Ошибка')
            print(e)

    def register(self):
        try:
            username = self.lineEdit.text()
            # Проверка, есть ли пользователь в базе
            if self.cur.execute(f"SELECT name FROM users WHERE name = '{username}'").fetchone() is None:
                all_users = [i for i in self.cur.execute(f"SELECT * FROM users")]
                if len(all_users) == 0:
                    self.cur.execute(f"INSERT INTO users VALUES (1, '{username}')")
                else:
                    self.cur.execute(f"INSERT INTO users VALUES ({all_users[-1][0] + 1}, '{username}')")
                self.label_3.setText('Успешная регистрация')
                self.db.commit()
            else:
                self.label_3.setText('Такой пользователь уже есть')
        except Exception as e:
            print(e)
        for value in self.cur.execute("""SELECT * FROM users"""):
            print(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Registration()
    ex.show()
    sys.exit(app.exec_())
