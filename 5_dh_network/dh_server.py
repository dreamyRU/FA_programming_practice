from random import randint

from fa_python_network.threaded_server import ThreadedServer
from dh import DH_Endpoint

class DHServer(ThreadedServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.public_key, self.private_key = (randint(1e3, 1e4) for _ in range(2))

    def handler(self, conn, addr):
        """
        DH object is created for each connection, which generates a secret key
        and allows you to encrypt and decrypt messages
        """
        print('Connected client', addr)
        DH = self.exchangeKeys(conn)

        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    print("Client disconnected", addr)
                    break

                print("Message from {} - {}".format(addr, data))
                data = DH.decrypt_message(data)
                print("Decrypt message from {} - {}".format(addr, data))

                res = DH.encrypt_message(data.upper())
                print("Send message - {}\n".format(res))
                conn.send(res.encode())

        except ConnectionAbortedError:
            print("Lost connection with", addr)
        finally:
            conn.close()

    def exchangeKeys(self, conn):
        DH = DH_Endpoint(self.public_key, None, self.private_key)
        DH.public_key2 = int(conn.recv(1024))
        conn.send(str(self.public_key).encode())

        partial_client_key = int(conn.recv(1024))
        conn.send(str(DH.generate_partial_key()).encode())

        DH.generate_full_key(partial_client_key)
        return DH

if __name__ == "__main__":
    try:
        server = DHServer("localhost", 9080)
        server.run()
    finally:
        server.stop()