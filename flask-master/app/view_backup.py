# -*- coding: utf-8 -*-

from flask import render_template, flash, get_flashed_messages, redirect
from flask import url_for, g, request, send_file

from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import get_debug_queries

from models import User, Survey1, Survey2, Survey5
from forms import LoginForm, RegistrationForm, Survey1Form, Survey2Form
from forms import Survey5Form, NewPass, ForgotPasswordForm
from email import user_notification, forgot_password
from config import DATABASE_QUERY_TIMEOUT, IMAGE_FILE_ROOT
from app import app, db, lm
from decorators import admin_required
from datetime import date
import uuid
from random import randint, shuffle
from img_info import IMAGE_TOTAL_NUM, DISTORTION_TYPES, DISTORTION_LEVELS, SHOW_TOTAL_NUM, SEQUENCE_NUM
import os
import linecache


@app.route('/survey_1/', methods=['GET', 'POST'])
@login_required
def survey_1():
    g.user = current_user
    if g.user.s1 is False:
        form = Survey1Form(request.form)

        if form.validate_on_submit():
            survey = Survey1()
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)

            g.user.s1 = True
            g.user.lastSeen = date.today()
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('survey/Survey1.html', title='Survey', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/survey_2/', methods=['GET', 'POST'])
@login_required
def survey_2():
    g.user = current_user
    if g.user.s1 is not False and g.user.s2 is False:
        form = Survey2Form(request.form)
        form.understand.data = True

        if form.validate_on_submit():
            survey = Survey2()
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)

            g.user.s2 = True
            g.user.lastSeen = date.today()
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('survey/Survey2.html', title='Survey', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/survey_5/', methods=['GET', 'POST'])
@app.route('/survey_5/<int:index>', methods=['GET', 'POST'])
@login_required
def survey_5():
    if g.user.s2 is not False and g.user.s5 is False:
        g.user = current_user
        # if g.user.s5 is False:
        form = Survey5Form(request.form)
        method = request.method
        if form.validate_on_submit():
            g.user.question_index += 1
            db.session.commit()
            question_index_show = g.user.question_index
            image_index, distortion_type, distortion_level = image_rendering1(
                question_index_show - 1, g.user.id)
            survey = Survey5(question_index=g.user.question_index,
                             image_index=image_index,
                             distortion_type=distortion_type,
                             distortion_level=distortion_level)
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)

            g.user.lastSeen = date.today()
            db.session.commit()
            if g.user.question_index >= SHOW_TOTAL_NUM:
                g.user.s5 = True
                db.session.commit()
                return render_template("final.html", title="Thanks!")
            else:
                return redirect(url_for('survey_5'))
        else:
            if g.user.question_index >= SHOW_TOTAL_NUM:
                g.user.s5 = True
                db.session.commit()
                return render_template("final.html", title="Thanks!")
            else:
                return survey_redering(form, method, g.user.id)
    else:
        return redirect(url_for('index'))


def survey_redering(form, method, user_id):
    if method == 'GET':
        question_index_show = g.user.question_index + 1
    else:
        question_index_show = g.user.question_index
    progress = float((question_index_show - 1)) / SHOW_TOTAL_NUM * 100

    image_index, distortion_type, distortion_level = image_rendering1(
        question_index_show - 1, user_id)
    filename1 = 'img/' + str(image_index) + '/source ' + \
        chr(40) + str(image_index) + chr(41) + '.png'
    filename2 = 'img/' + str(image_index) + '/source (' + str(image_index) + ')' + \
        '_' + distortion_type + '_' + str(distortion_level) + '.png'

    if question_index_show < SHOW_TOTAL_NUM:
        image_index_next, distortion_type_next, distortion_level_next = image_rendering1(
            question_index_show, user_id)
        filename1_next = 'img/' + str(image_index_next) + '/source ' + \
            chr(40) + str(image_index_next) + chr(41) + '.png'
        filename2_next = 'img/' + str(image_index_next) + '/source (' + str(image_index_next) + ')' + \
            '_' + distortion_type_next + '_' + str(distortion_level_next) + '.png'
    else:
        filename1_next = filename1
        filename2_next = filename2
    return render_template('survey/Survey5.html', title='Survey', 
        question_index=question_index_show, filename1=filename1, 
        filename2=filename2, form=form, progress=progress,
        filename1_next=filename1_next, filename2_next=filename2_next)


# def image_rendering(question_index):
#     if (question_index - 1) % IMAGE_TOTAL_NUM == 0:
#         g.user.image_mark_array = ''.join(['0'] * IMAGE_TOTAL_NUM)
#         image_index = 0 if (g.user.distortion_index_last == IMAGE_TOTAL_NUM - 1) else (g.user.distortion_index_last + 1)
#     else:
#         image_index = randint(0, IMAGE_TOTAL_NUM - 1)
#         while g.user.image_mark_array[image_index] == '1':
#             image_index = randint(0, IMAGE_TOTAL_NUM - 1)

#     image_mark_array_tmp = list(g.user.image_mark_array)
#     image_mark_array_tmp[image_index] = '1'
#     g.user.image_mark_array = ''.join(image_mark_array_tmp)

#     g.user.distortion_index_last = image_index

#     db.session.commit()
#     distortion_type = 'barrel'
#     distortion_level = 1
#     image_index = image_index + 1
#     return (image_index, distortion_type, distortion_level)


def image_rendering1(question_index, user_id):
    filename = str(user_id) + '.txt'
    line = linecache.getline(filename, question_index + 1)
    app.logger.debug("line = %s", line)

    params = line.split()
    image_index = params[0]
    distortion_type = params[1]
    distortion_level = params[2]
    return (image_index, distortion_type, distortion_level)


@app.route('/create_acct/', methods=['GET', 'POST'])
def create_acct():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data,
                    oldPassword=form.password.data, userid=(str(uuid.uuid1())), 
                    image_mark_array=''.join(['0'] * IMAGE_TOTAL_NUM))
        db.session.add(user)
        db.session.commit()
        login_user(user)

        # create a image display sequence for the present user
        user_id = user.id
        with open(os.path.join(IMAGE_FILE_ROOT, 'workfile.txt')) as f:
            lines = f.readlines()
            f.close()
        shuffle(lines)
        with open(os.path.join(IMAGE_FILE_ROOT, str(user_id) + '.txt'), 'w+') as g:
            g.writelines(lines)
            g.close()

        # user_notification(user)
        return redirect(url_for('index'))
    return render_template('create_acct.html', title="Create Account", form=form)


@app.route('/new_pass/', methods=['GET', 'POST'])
def new_pass():
    form = NewPass(request.form)
    if form.validate_on_submit():
        user = g.user
        print(form.data)
        if user.password == form.data['password']:
            print('I should raise a validation error')
            form.password.errors.append(
                'You\'ve already used this password. Please choose a new password.')
        else:
            print('user picked a different password')
            user.password = form.password.data
            user.changedPass = True
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('new_pass.html', title='Update Password', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        user = g.user
        if current_user.is_admin():
            return redirect(url_for('admin'))
        else:
            return redirect(request.args.get("next") or url_for("index"))
    return render_template('login.html', title="Login", form=form)


@app.route('/forgot_passwd', methods=['GET', 'POST'])
def forgot_passwd():
    form = ForgotPasswordForm(request.form)
    if form.validate_on_submit():
        user = request.form['email']
        if User.query.filter_by(email=user).first():
            q = User.query.filter_by(email=user).first()
            login_user(q)
            user = g.user
            # forgot_password(user, q.password)
            app.logger.debug('ready to change the password')
            return redirect(request.args.get("next") or url_for("new_pass"))
        else:
            flash('Username not found', 'error')
            # return redirect(request.args.get("next") or url_for("login"))
    return render_template("forgot_passwd.html",
                           title="Forgot Password",
                           form=form)


@app.route('/')
@app.route('/index')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = g.user
    if user.is_admin():
        return redirect(url_for('admin'))
    return render_template("index.html", title="Home", user=user)
    # if user.lastSeen != str(date.today()):
    #   return render_template ("index.html",
    #       title = "Home",
    #       user = user)
    # else:
    # return render_template("comeback.html", title="Please come back later",
    # user=user)


@app.route('/consent/')
def consent():
    return render_template('consent.html', title="Consent")


@app.route('/logouthtml/')
def logouthtml():
    return render_template('logout.html', title="Logout")


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/restart')
@login_required
def restart():
    g.user.s1 = False
    g.user.s2 = False
    g.user.s5 = False
    g.user.question_index = 0
    g.user.distortion_index_last = -1
    g.usermage_mark_array = ''.join(['0'] * IMAGE_TOTAL_NUM)
    db.session.query(Survey1).filter_by(user_id=g.user.id).delete()
    db.session.query(Survey2).filter_by(user_id=g.user.id).delete()
    db.session.query(Survey5).filter_by(user_id=g.user.id).delete()
    # Survey1.query.filter(Survey1.user_id = g.user.email).delete()
    # Survey2.query.filter(Survey2.user_id = g.user.email).delete()
    # Survey5.query.filter(Survey5.user_id = g.user.email).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete')
@login_required
@admin_required
def delete(email):
    user = User.query.filter_by(email=email).first()
    user_id = user.id
    app.logger.debug(user)
    db.session.query(Survey1).filter_by(user_id=user_id).delete()
    db.session.query(Survey2).filter_by(user_id=user_id).delete()
    db.session.query(Survey5).filter_by(user_id=user_id).delete()
    db.session.query(User).filter_by(email=email).delete()
    db.session.commit()
    # return redirect(url_for('index'))


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                               (query.statement, query.parameters, query.duration, query.context))
    return response


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    method = request.method
    app.logger.debug('admin page')
    app.logger.debug(method)
    if request.method == 'GET':
        app.logger.debug('get the admin page')
        users = User.query.filter_by(role=0)
        return render_template('admin/index.html', title="Admin", users=users)
    else:
        app.logger.debug('post the admin page')
        users_delete = request.form.getlist('check')
        for user in users_delete:
            app.logger.debug(user)
            delete(user)
        users = User.query.filter_by(role=0)
        return render_template('admin/index.html', title="Admin", users=users)


@app.route('/admin_survey1/')
@login_required
@admin_required
def admin_survey1():
    surveys = Survey1.query.all()
    return render_template('admin/partials/survey1.html', title='Admin Survey-1', surveys=surveys)


@app.route('/admin_survey2/')
@login_required
@admin_required
def admin_survey2():
    surveys = Survey2.query.all()
    return render_template('admin/partials/survey2.html', title='Admin Survey-2', surveys=surveys)


@app.route('/admin_survey3/')
@login_required
@admin_required
def admin_survey3():
    surveys = Survey3.query.all()
    return render_template('admin/partials/survey3.html', title='Admin Survey-3', surveys=surveys)


@app.route('/admin_survey4/')
@login_required
@admin_required
def admin_survey4():
    surveys = Survey4.query.all()
    return render_template('admin/partials/survey4.html', title='Admin Survey-4', surveys=surveys)


@app.route('/admin_survey5/')
@login_required
@admin_required
def admin_survey5():
    surveys = Survey5.query.all()
    return render_template('admin/partials/survey5.html', title='Admin Survey-5', surveys=surveys)
