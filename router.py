from flask import Flask, render_template, request, jsonify
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from database.signup import *
import json
import urllib.parse
from datetime import datetime, timedelta


class Router:
    signup = Signup()

    def __init__(self, app, token_required) -> None:
        self.app = app
        self.token_required = token_required

    def serve(self):
        @self.app.route("/")
        def home():
            return render_template('signin.html')

        @self.app.route("/signin")
        def signin():
            return render_template('signin.html')

        @self.app.route("/register")
        def register():
            return render_template('signup.html')

        @self.app.route("/user_signup", methods=['POST'])
        def user_signup():
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]
            password = params_dict['password'][0]

            status = self.signup.register(username, generate_password_hash(password))
            return {'status': status}

        @self.app.route("/check_username_availability", methods=['POST'])
        def check_username_availability():
            # username = request.json['username']
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]

            status = self.signup.check_username_availability(username)
            
            return {'status': status}

        @self.app.route("/user_signin", methods=['POST'])
        # @self.token_required
        def user_signin():
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]
            password = params_dict['password'][0]

            status, user_dict = self.signup.verify_user(username, password)
            token = ''
            if status:
                token = jwt.encode({
                    'public_id': user_dict['pid'],
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                }, self.app.config['SECRET_KEY'])

            return {'status': status, 'token': token, 'user': user_dict}

        # @self.app.route("/dashboard", methods=['GET'])
        # @self.token_required
        # def dashboard():
        #     return render_template('dashboard.html')

        # @self.app.route("/user_dashboard", methods=['POST'])
        # @self.token_required
        # def user_dashboard():
        #     return {'status': True, 'auth': True}
        

        @self.app.route("/oltp", methods=['GET'])
        @self.token_required
        def oltp():
            return render_template('oltp.html')
        

        @self.app.route("/process_olt", methods=['POST'])
        @self.token_required
        def process_olt():
            return {'status': True, 'auth': True}

        @self.app.route("/oltp_no_auth", methods=['GET'])
        # @self.token_required
        def oltp_no_auth():
            return render_template('oltp.html')

        @self.app.route("/process_olt_no_auth", methods=['POST'])
        # @self.token_required
        def process_olt_no_auth():
            return {'status': True, 'auth': True}
