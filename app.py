from flask import Flask, request, jsonify
import jwt
import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meowmeow123'  # Secret key for JWT encoding


# Root route
@app.route('/')
def index():
    return jsonify({"title": "JWT Demo"})


# Get account data from JSON server
def get_account(username):
    response = requests.get(
        f'http://localhost:5000/accounts?username={username}'
    )
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return None


# Route to authenticate and get JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    account = get_account(username)
    if account and account['password'] == password:
        # Generate JWT token
        token = jwt.encode({
            'userId': account['id'],
            'exp': datetime.datetime.now(
                datetime.UTC
            ) + datetime.timedelta(
                minutes=5
            )
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401


# Route to check permission with JWT
@app.route('/check_permission', methods=['POST'])
def check_permission():
    token = request.headers.get('Authorization').split(" ")[1]
    permission_required = request.json.get('permission')

    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256']
        )
        userId = decoded_token['userId']

        # Fetch the user's permissions from the JSON server
        response = requests.get(
            f'http://localhost:5000/permissions?id={userId}'
        )
        if response.status_code == 200 and response.json():
            user_permissions = response.json()[0]['permissions']

            if permission_required in user_permissions:
                return jsonify({'message': 'Permission granted'})
            else:
                return jsonify({'message': 'Permission denied'}), 403

        return jsonify({'message': 'User not found'}), 404

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(debug=True)
