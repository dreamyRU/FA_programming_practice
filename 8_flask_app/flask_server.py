from datetime import datetime
from flask import Flask, request
import json
import hashlib

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def registerUser():
    users = load_users()
    login = request.form.get('login')
    password = request.form.get('password')
    try:
        users[login]
        return {'status': 'error, this user already exists'}, 400
    except KeyError:
        users[login] = {}
        users[login]['password'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
        users[login]['date'] = str(datetime.now())
        
    save_users(users)
    return {'status': 'success'}, 200

@app.route('/user', methods=['GET'])
def getUsers():
    users = load_users()
    if not users:
        return {'status': 'no registered users'}
    return load_users()

def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
