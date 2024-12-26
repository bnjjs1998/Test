from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
from login_route import *
#je vais configurer mongo
from model import *
from route import *


if __name__ == '__main__':
    app.run(debug=True)
