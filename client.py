from socket import AF_INET, SOCK_STREAM, socket
import threading


class Client:
    def __init__(self):
        self.nickname = None
        self.host = '127.0.0.1'
        self.port = 8080
        self.__start_client()

    def __start_client(self):
        try:
            self.nickname = input("Choose your nickname: ")
            self.client_instance = socket(AF_INET, SOCK_STREAM)
            self.client_instance.connect((self.host, self.port))
        except ConnectionRefusedError:
            print('Server is not running!')

    def receive(self):
        while True:
            try:
                message = self.client_instance.recv(1024).decode('ascii')
                if message == 'NICKNAME':
                    self.client_instance.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except ConnectionError:
                print("An error occured!")
                self.client_instance.close()
                break

    def write(self):
        while True:  # message layout
            message = '{}: {}'.format(self.nickname, input(''))
            self.client_instance.send(message.encode('ascii'))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()


if __name__ == '__main__':
    client = Client()
    client.run()
