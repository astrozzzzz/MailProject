import socket
import sqlite3


from threading import Thread
from db_work import DBHandler


codes = {
    '001': 'check user',
    '002': 'insert user',
    '031': 'sender',
    '032': 'addressee',
    '033': 'title',
    '034': 'main text'
}


class MailServer:
    def __init__(self):
        # Инициализация сервера
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server.bind(("127.0.0.1", 1234))
        self.server.listen()
        print('Server is listening')

        # Подключение базы данных
        self.db = DBHandler()

        self.mail = []

    def server_work(self, user, data):
        action = codes[data[:3]]
        if action == 'check user':
            if self.db.check_user(data[3:]):
                user.send("500".encode("utf-8"))
            else:
                user.send("404".encode("utf-8"))
        elif action == 'insert user':
            result = self.db.insert_user(data[3:])
            if result:
                user.send("500".encode("utf-8"))
            else:
                user.send("404".encode("utf-8"))
        elif action == 'sender' or action == 'addressee' or action == 'title' or action == 'main text':
            print('initialized username')
            self.mail.append(data[:3])
            if action == 'main text':
                self.db.insert_mail(self.mail[0], self.mail[1], self.mail[2], self.mail[3])
                print('db username')

    def listen_user(self, user):
        while True:
            try:
                data = user.recv(2048).decode("utf-8")
                if len(data) != 0:
                    action = codes[data[:3]]
                    if action == 'check user':
                        if self.db.check_user(data[3:]):
                            user.send("500".encode("utf-8"))
                        else:
                            user.send("404".encode("utf-8"))
                    elif action == 'insert user':
                        result = self.db.insert_user(data[3:])
                        if result:
                            user.send("500".encode("utf-8"))
                        else:
                            user.send("404".encode("utf-8"))
                    elif action == 'sender' or action == 'addressee' or action == 'title' or action == 'main text':
                        print('initialized username')
                        self.mail.append(data[3:])
                        if action == 'main text':
                            self.db.insert_mail(self.mail[0], self.mail[1], self.mail[2], self.mail[3])
                            print('db username')
            except Exception as e:
                print(e)

    def start_server(self):
        while True:
            user_socket, address = self.server.accept()
            print('User connected')
            user_thread = Thread(target=self.listen_user, args=(user_socket,))
            user_thread.start()


server = MailServer()
server.start_server()
