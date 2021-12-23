import requests

def getUsers():
    r = requests.get('http://127.0.0.1:5000/user')
    return r.status_code, r.json()

if __name__ == '__main__':
    users = getUsers()
    print(users)