# -*- coding: utf-8 -*-

import os

PROJECT = "survey"

# Get app root path, also can use flask.root_path
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATABASE_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/app/static/database'
IMAGE_FILE_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/app/static/img-display-protocol'


DEBUG = True
TESTING = False

ADMINS = ['zhangboknight@gmail.com']

# http://flask.pocoo.org/docs/quickstart/#sessions
SECRET_KEY = 'youshouldreplacethis'

SQLALCHEMY_ECHO = False
DATABASE_QUERY_TIMEOUT = 15
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_ROOT + '/%s.sqlite' % PROJECT

MAIL_DEBUG = DEBUG
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'zhangboknight'
MAIL_PASSWORD = 'zhangmozhe'
DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME
