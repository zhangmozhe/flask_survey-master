# -*- coding: utf-8 -*-

import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/static/img-display-protocol/')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

mail = Mail(app)

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=31)


import views
import models
import index_script
