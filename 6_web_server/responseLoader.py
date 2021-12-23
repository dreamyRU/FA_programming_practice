class ResponseLoader:
    def __init__(self):
        self.paths = {
            '/': 'index.html',
            '/about': 'about.html',
            '/content': 'content.html',
            '/style/main.css': 'main.css'
        }

    def loadResponse(self, path):
        header = 'HTTP/1.1 200 OK\n'
        contentType = ''
        try:
            file = self.paths[path]
            if file.endswith('.html'):
                contentType = 'text/html'
                file = 'public/' + file

            elif file.endswith('.css'):
                contentType = 'text/css'
                file = 'style/' + file

            else:
                header = 'HTTP/1.1 403 Forbidden\n\n'
                file = 'public/403.html'

        except KeyError:
            header = 'HTTP/1.1 404 File not found\n\n'
            file = 'public/404.html'

        with open(file, 'r') as f:
            content = f.read()
        
        if not contentType:
            return header + content

        return header + 'Content-Type: ' + contentType + '\n\n' + content
