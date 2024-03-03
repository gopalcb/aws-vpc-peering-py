"""
FLASK api entry point
run on port: 5000

Author: Gopal Chandra Bala
"""

from flask import Flask, render_template
import sqlite3 
from functools import wraps
from router import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'app-secret-key'

connect = sqlite3.connect('database.db') 
connect.execute('CREATE TABLE IF NOT EXISTS users (pid TEXT, username TEXT, password TEXT)')


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            connect = sqlite3.connect('database.db') 
            cursor = connect.cursor() 
            cursor.execute(f'SELECT * FROM users WHERE pid={data['pid']}')
            data = cursor.fetchall()
            pid, username, password = data[0]
            current_user = {
                'pid': pid,
                'username': username,
                # 'password': password
            }

        except Exception as e:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
  
    return decorated


# configure api routes in a single file
router = Router(app, token_required)
router.serve()


if __name__ == "__main__":
    app.run()
