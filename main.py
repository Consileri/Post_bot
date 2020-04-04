from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from flask_restful import Api
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
