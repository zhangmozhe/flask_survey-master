# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from app import app, db

from app.models import User
# from flask.ext.profile import Profiler

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

from app.index_script import generate_index, clear_index

manager = Manager(app)
manager.add_option('-c', '--config', dest='config', required=False)
# Profiler(app)



@manager.command
def initdb():
    """initialize database"""
    db.drop_all()
    db.create_all()

    admin = User(
        username=u'zhangboknight@gmail.com',
        email=u'zhangboknight@gmail.com',
        password=u'zhangmozhe',
        role=1)
    db.session.add(admin)
    db.session.commit()

    clear_index()
    generate_index()


if __name__ == "__main__":
    manager.run()
