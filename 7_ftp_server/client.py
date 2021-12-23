from random import randint

from fa_python_network.client import Client

if __name__ == '__main__':
    client = Client('localhost', randint(2000, 10000))
    try:
        client.connect('localhost', 9080)
    finally:
        client.closeSocket()