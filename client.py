from socket import AF_INET, SOCK_STREAM, socket
import threading


class Client:
    def __init__(self):
        self.nickname = None
        self.listening = True
        self.host = '127.0.0.1'
        self.port = 3333
        self.__start_client()

    def close(self):
        self.server_instance.close()

    def list_all_users(self):
        self.server_instance.send(f'{self.nickname}: /list'.encode('ascii'))

    def __start_client(self):
        try:
            self.nickname = input("Choose your nickname: ")
            self.server_instance = socket(AF_INET, SOCK_STREAM)
            self.server_instance.connect((self.host, self.port))
            self.server_instance.send(self.nickname.encode('ascii'))
        except ConnectionRefusedError:
            print('Server is not running!')

    def receive(self):
        while self.listening:
            try:
                message = self.server_instance.recv(1024).decode('ascii')
                print(message)
            except ConnectionError:
                print("An error occured!")
                self.server_instance.close()
                break

    def write(self):
        while True:
            content = input('')
            message = '{}: {}'.format(self.nickname, content)
            self.server_instance.send(message.encode('ascii'))
            if content == '/quit':
                self.server_instance.close()
                self.listening = False
                break

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()


if __name__ == '__main__':
    client = Client()
    client.run()
