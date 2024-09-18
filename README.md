# JWT Demo

### Requirements
- `npm i -g json-server`
- `pip install flask pyjwt requests`

### JWT (Json Web Token)

A token will be generate with using id, expiration time and secret key
```py
token = jwt.encode({
	'userId': account['id'],
	'exp': datetime.datetime.now(
		datetime.UTC
	) + datetime.timedelta(
		minutes=5
	)
}, app.config['SECRET_KEY'], algorithm='HS256')
```

### How to run

1. Start json-server
```bash
json-server --watch db.json --port 5000
```
2. Open a different terminal and run app.py
```bash
python app.py
```
3. Open another terminal and use this command to log in
```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "john_doe", "password": "password123"}'
```
A token will be printed on console

4. If you haven't modified the secret key, test `check_permission` with this command

```bash
curl -X POST http://127.0.0.1:5000/check_permission \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImV4cCI6MTcyNjY3MjQ5N30.cM0N729j6x32LWIX187MoQZs6da4CVh401ARSvJ2fBU" \
-H "Content-Type: application/json" \
-d '{"permission": "write"}'
```
Otherwise, replace this token with the one you get after logging in

`"Authorization: Bearer your_token_here"`

[More about JWT and its libraries](https://jwt.io/)
