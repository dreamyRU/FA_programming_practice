from random import randint

from fa_python_network.client import Client
from dh import DH_Endpoint

class DHClient(Client):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.public_key, self.private_key = (randint(1e3, 1e4) for _ in range(2))
        self.DH = DH_Endpoint(None, self.public_key, self.private_key)

    def connect(self, host, port):
        self.sock.connect((host, port))
        self.exchange_keys()
        while True:
            msg = input("Enter message:")
            if not msg:
                break

            msg = self.DH.encrypt_message(msg)
            print("Sending encrypted message -", msg)
            self.sock.send(msg.encode())

            data = self.sock.recv(1024).decode()
            print("Message from the server - {}".format(data))
            data = self.DH.decrypt_message(data)
            print("Decrypted message from the server - {}\n".format(data))

    def exchange_keys(self):
        self.sock.send(str(self.public_key).encode())

        self.DH.public_key1 = int(self.sock.recv(1024))
        self.sock.send(str(self.DH.generate_partial_key()).encode())

        server_partial_key = int(self.sock.recv(1024))
        self.DH.generate_full_key(server_partial_key)


if __name__ == "__main__":
    try:
        client = DHClient("localhost", randint(2000, 10000))
        client.connect("localhost", 9080)
    finally:
        client.closeSocket()