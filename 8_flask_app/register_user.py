import requests

def registerUser(login, password):
    r = requests.post('http://127.0.0.1:5000/user', data={
        'login': login,
        'password': password
    })
    return r.status_code, r.json()

if __name__ == '__main__':
    login = input("Enter login:")
    password = input("Enter password:")
    status = registerUser(login, password)
    print(status)
    