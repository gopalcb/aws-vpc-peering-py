import sqlite3 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class Signup:
    def __init__(self) -> None:
        pass

    def register(self, username, password):
        try:
            with sqlite3.connect("database.db") as context: 
                cursor = context.cursor() 
                cursor.execute("INSERT INTO users (pid, username, password) VALUES (?,?,?)", (str(uuid.uuid4()), username, generate_password_hash(password)))
                context.commit()

            return True

        except Exception as e:
            print(f'error: {e}')
            return False

    def check_username_availability(self, username):
        try:
            connect = sqlite3.connect('database.db') 
            cursor = connect.cursor() 
            cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
            data = cursor.fetchall()
            if data:
                pid, username, password = data[0]
                print(f'data: {data[0]}')
                return False
            else:
                return True

        except Exception as e:
            print(f'error: {e}')
            return False

    def verify_user(self, username, password):
        try:
            connect = sqlite3.connect('database.db') 
            cursor = connect.cursor() 
            cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
            data = cursor.fetchall()
            if data:
                pid, username, xpassword = data[0]
                user_dict = {'pid': pid, 'username': username}
                if check_password_hash(xpassword, password):
                    print(f'data: {data}')
                    return True, user_dict
                else:
                    return False, None
            else:
                return False, None

        except Exception as e:
            print(f'error: {e}')
            return False, None
