import sys
import socket

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import uic
from write_mail import MailForm
from db_work import DBHandler


class Client(QWidget):
    def __init__(self, client, username):
        super().__init__()
        self.client = client
        self.username = username

        # Подключаем дизайн
        uic.loadUi('design/main_window.ui', self)
        self.setWindowTitle('Почта')
        self.label_11.setText(username)

        # Коннект кнопок
        self.pushButton.clicked.connect(self.write_mail)

    # Диалоговое окно написания письма
    def write_mail(self, errors=None, content=None):
        self.hide()
        self.ex = MailForm()
        # Если была ошибка
        print(errors)
        if errors is not False:
            self.ex.addressee.setText(content[0])
            self.ex.title.setText(content[1])
            self.ex.main_text.setText(content[2])
            if 'blank user' in errors:
                self.ex.label_not_found.setText('Заполните поле')
                self.ex.label_not_found.setVisible(True)
            elif 'not found' in errors:
                self.ex.label_not_found.setText('Пользователь не найден')
                self.ex.label_not_found.setVisible(True)
            if 'blank title' in errors:
                self.ex.label_title_error.setText('Заполните поле')
                self.ex.label_title_error.setVisible(True)
            if 'blank main text' in errors:
                self.ex.label_error.setText('Заполните поле')
                self.ex.label_error.setVisible(True)
        result_dialog = self.ex.exec()
        if result_dialog == QDialog.Rejected:
            self.show()
        elif result_dialog == QDialog.Accepted:
            print('Accepted')
            errors = []
            # Проверка данных
            if len(self.ex.addressee.text()) == 0:
                errors.append('blank user')
            message = '001' + self.ex.addressee.text()
            self.client.send(message.encode('utf-8'))
            response = self.client.recv(2048).decode("utf-8")
            if response != '500':
                errors.append('not found')
            if len(self.ex.title.text()) == 0:
                errors.append('blank title')
            if len(self.ex.main_text.toPlainText()) == 0:
                errors.append('blank main text')
            if len(errors) != 0:
                data = [self.ex.addressee.text(), self.ex.title.text(), self.ex.main_text.toPlainText()]
                self.write_mail(errors, data)
            # Если ошибки не было
            else:
                print('ok')
                message = '031' + self.username
                self.client.send(message.encode('utf-8'))
                print('sent username')
                message = '032' + self.ex.addressee.text()
                self.client.send(message.encode('utf-8'))
                message = '033' + self.ex.title.text()
                self.client.send(message.encode('utf-8'))
                message = '034' + self.ex.main_text.toPlainText()
                self.client.send(message.encode('utf-8'))



