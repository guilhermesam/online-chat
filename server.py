from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket


class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.__start_server()
        self.clients = []
        self.nicknames = []

    def __start_server(self):
        self.server_instance = socket(AF_INET, SOCK_STREAM)
        self.server_instance.bind((self.host, self.port))
        self.server_instance.listen()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except ConnectionError:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('ascii'))
                self.nicknames.remove(nickname)
                break

    def run(self):
        while True:
            client, address = self.server_instance.accept()
            client.send('NICKNAME'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)
            self.broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            thread = Thread(target=self.handle, args=(client,))
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.run()
