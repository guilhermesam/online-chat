from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket


class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3333
        self.__start_server()
        self.clients = []
        self.nicknames = []

    def __start_server(self):
        self.server_instance = socket(AF_INET, SOCK_STREAM)
        self.server_instance.bind((self.host, self.port))
        self.server_instance.listen()
        print(f'Server is running on {self.host}:{self.port}')

    def list_all_users(self):
        return '\n'.join(self.nicknames).encode('ascii')

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def quit(self, client):
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        nickname = self.nicknames[index]
        self.broadcast('{} left!'.format(nickname).encode('ascii'))
        self.nicknames.remove(nickname)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                content = message.decode('ascii').split(' ')[1]
                if content == '/quit':
                    self.quit(client)
                    break
                elif content == '/list':
                    self.broadcast(self.list_all_users())
                else:
                    self.broadcast(message)
            except ConnectionError:
                break

    def run(self):
        while True:
            connection, address = self.server_instance.accept()
            nickname = connection.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(connection)
            self.broadcast("{} joined!".format(nickname).encode('ascii'))
            # connection.send('Connected to server!'.encode('ascii'))
            thread = Thread(target=self.handle, args=(connection,))
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.run()
