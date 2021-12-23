from fa_python_network.threaded_server import ThreadedServer
from responseLoader import ResponseLoader

class WebServer(ThreadedServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.responseLoader = ResponseLoader()

    def handler(self, conn, addr):
        try:
            print('Connected client', addr)
   
            request = conn.recv(8192).decode()
            headers = request.split()

            response = self.responseLoader.loadResponse(headers[1])
            conn.send(response.encode('utf-8'))
        finally:
            conn.close()
    

if __name__ == "__main__":
    try:
        webserver = WebServer("localhost", 8080)
        webserver.run()
    finally:
        webserver.stop()