from flask import Flask, render_template, request, jsonify
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from oltp.payment_processing import *
import json
import urllib.parse
from datetime import datetime, timedelta


class Router:
    payment_processing = PaymentProcessing()

    def __init__(self, app, token_required=None) -> None:
        self.app = app
        self.token_required = token_required

    def serve(self):

        @self.app.route("/process_payment", methods=['POST'])
        def process_payment():
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]
            password = params_dict['password'][0]

            status = self.signup.register(username, generate_password_hash(password))
            return {'status': status}

        @self.app.route("/post_payment", methods=['POST'])
        def post_payment():
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]
            password = params_dict['password'][0]

            status = self.signup.register(username, generate_password_hash(password))
            return {'status': status}

        @self.app.route("/payment_success", methods=['POST'])
        def payment_success():
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]
            password = params_dict['password'][0]

            status = self.signup.register(username, generate_password_hash(password))
            return {'status': status}

        @self.app.route("/payment_error", methods=['POST'])
        def payment_error():
            params_dict = urllib.parse.parse_qs(request.data.decode())
            username = params_dict['username'][0]
            password = params_dict['password'][0]

            status = self.signup.register(username, generate_password_hash(password))
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
