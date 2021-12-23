import os

class FileManager:
    def __init__(self, root):
        self.root = root + '/'

    def showFiles(self):
        files = os.listdir(self.root)
        if not files:
            return 'The folder is empty'

        return ' '.join(os.listdir(self.root))
    
    def exists(self, name):
        if name in os.listdir(self.root):
            return True
        return False

    def createFolder(self, name):
        if self.exists(name):
            return 'This folder already exists'

        os.mkdir(self.root + name)
        return 'The folder created successfully'    
        

    def removeFolder(self, name):
        try:
            if self.exists(name):
                os.rmdir(self.root + name)
                return 'The folder removed successfully'
            return 'This folder does not exist'

        except NotADirectoryError:
            return f'{name} is not a directory'
    
    def createFile(self, name):
        if self.exists(name):
            return 'This file already exists'
        
        with open(self.root + name, 'w') as f:
            f.write('')
        return 'The file created successfully'

    def removeFile(self, name):
        if not self.exists(name):
            return 'This file does not exist'
        elif os.path.isdir(self.root + name):
            return "You can not remove a folder with 'rm', use 'rmdir' instead."
        
        os.remove(self.root + name)
        return 'This file removed successfully'
        
    def writeFile(self, name, text):
        if self.exists(name) and os.path.isdir(self.root + name):
            return "You can't write text to folder"
        
        with open(self.root + name, 'w') as f:
            f.write(text)
        return 'Text written to the file successfully'
    
    def readFile(self, name):
        if not self.exists(name):
            return 'This file does not exist'
        if os.path.isdir(self.root + name):
            return "You can't read folder with this command"
        
        with open(self.root + name, 'r') as f:
            content = f.read()
        if not content:
            return 'The file is empty'

        return content

    def renameFile(self, old_name, new_name):
        if not self.exists(old_name):
            return 'This file does not exist'

        os.rename(self.root + old_name, self.root + new_name)
        return 'The file was renamed successfully'