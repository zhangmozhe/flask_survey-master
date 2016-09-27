web: python flask-master/manage.py runserver
web: gunicorn manager.wsgi --log-file -
heroku ps:scale web=1