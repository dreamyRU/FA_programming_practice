from fa_python_network.threaded_server import ThreadedServer
from fileManager import FileManager

class FTPServer(ThreadedServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.fileManager = FileManager("WorkingDirectory")

    def handler(self, conn, addr):
        print('Connected client', addr)
        try:
            while True:
                msg = conn.recv(1024).decode()
                if not msg:
                    print("Client disconnected", addr)
                    break

                print("Message from {} - {}".format(addr, msg))

                response = self.load_response(msg)
                conn.send(response.encode())
        except ConnectionAbortedError:
            print("Lost connection with", addr)
        finally:
            conn.close()

    def load_response(self, msg):
        response = ''
        msg = msg.split()

        if len(msg) == 1:
            if msg[0] == 'ls':
                response = self.fileManager.showFiles()
        elif len(msg) == 2:
            command, name = msg[0], msg[1]
            if command == 'mkdir':
                response = self.fileManager.createFolder(name)
            elif command == 'rmdir':
                response = self.fileManager.removeFolder(name)
            elif command == 'touch':
                response = self.fileManager.createFile(name)
            elif command == 'rm':
                response = self.fileManager.removeFile(name)
            elif command == 'cat':
                response = self.fileManager.readFile(name)
        elif len(msg) > 2:
            if msg[0] == 'nano':
                response = self.fileManager.writeFile(msg[1], ' '.join(msg[2:]))
            elif msg[0] == 'rename':
                response = self.fileManager.renameFile(msg[1], msg[2])
        if not response:
            response = 'command not found'
        return response + '\n'


if __name__ == '__main__':
    ftpserver = FTPServer('localhost', 9080)
    try:
        ftpserver.run()
    finally:
        ftpserver.stop()