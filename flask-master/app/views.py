# -*- coding: utf-8 -*-

from flask import render_template, flash, get_flashed_messages, redirect
from flask import url_for, g, request, send_file

from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import get_debug_queries

from models import User, Survey1, Survey2, Survey5, Comment
from forms import LoginForm, RegistrationForm, Survey1Form, Survey2Form, CommentForm
from forms import Survey5Form, NewPass, ForgotPasswordForm
from email import user_notification, forgot_password
from config import DATABASE_QUERY_TIMEOUT, IMAGE_FILE_ROOT, DATABASE_ROOT
from app import app, db, lm
from decorators import admin_required
import datetime
import uuid
from random import randint, shuffle
from img_info import SOURCE_PER_GROUP, IMAGE_PER_GROUP, DISTORTION_TYPES, DISTORTION_LEVELS, IMAGE_NUM, IMG_SERVER, GROUP_NUM
import os
import linecache
import pygeoip


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
            # g.user.lastSeen = date.today()
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('survey/Survey1.html', title='Survey', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/survey_2_next/', methods=['GET', 'POST'])
@login_required
def survey_2_next():
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
            # g.user.lastSeen = date.today()
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('survey/Survey2_next.html', title='Survey', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/survey_2/', methods=['GET', 'POST'])
@login_required
def survey_2():
    g.user = current_user
    if g.user.s1 is not False and g.user.s2 is False:
        return render_template('survey/Survey2.html', title='Survey')
    else:
        return redirect(url_for('index'))


@app.route('/survey_5/', methods=['GET', 'POST'])
@app.route('/survey_5/<int:index>', methods=['GET', 'POST'])
@login_required
def survey_5():
    if g.user.s2 is not False and g.user.s5 is False:
        g.user = current_user
        form = Survey5Form(request.form)
        method = request.method
        if form.validate_on_submit():
            g.user.question_index += 1
            db.session.commit()
            question_index_show = g.user.question_index
            image_index, distortion_type, distortion_level = image_index_rendering(
                question_index_show - 1, g.user.id, g.user.group)
            survey = Survey5(question_index=g.user.question_index,
                             image_index=image_index,
                             distortion_type=distortion_type,
                             distortion_level=distortion_level)
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)

            # g.user.lastSeen = date.today()
            db.session.commit()
            if g.user.question_index >= IMAGE_PER_GROUP:
                g.user.s5 = True
                db.session.commit()
                return redirect(url_for('final'))
            else:
                return redirect(url_for('survey_5'))
        else:
            if g.user.question_index >= IMAGE_PER_GROUP:
                g.user.s5 = True
                db.session.commit()
                return redirect(url_for('final'))
            else:
                return survey_redering(form, method, g.user.id, g.user.group)
    else:
        return redirect(url_for('index'))


def survey_redering(form, method, user_id, group_index):
    if method == 'GET':
        question_index_show = g.user.question_index + 1
    else:
        question_index_show = g.user.question_index
    progress = float((question_index_show - 1)) / IMAGE_PER_GROUP * 100

    image_index, distortion_type, distortion_level = image_index_rendering(
        question_index_show - 1, user_id, group_index)
    filename1 =  'img/' + str(image_index) + '/source ' + \
        chr(40) + str(image_index) + chr(41) + '.png'
    filename2 = 'img/' + str(image_index) + '/source (' + str(image_index) + ')' + \
        '_' + distortion_type + '_' + str(distortion_level) + '.png'

    if question_index_show < IMAGE_PER_GROUP:
        image_index_next, distortion_type_next, distortion_level_next = image_index_rendering(
            question_index_show, user_id, group_index)
        filename1_next = 'img/' + str(image_index_next) + '/source ' + \
            chr(40) + str(image_index_next) + chr(41) + '.png'
        filename2_next = 'img/' + str(image_index_next) + '/source (' + str(image_index_next) + ')' + \
            '_' + distortion_type_next + '_' + \
            str(distortion_level_next) + '.png'
    else:
        filename1_next = filename1
        filename2_next = filename2
    return render_template('survey/Survey5.html', title='Survey',
                           question_index=question_index_show, filename1=filename1,
                           filename2=filename2, form=form, progress=progress,
                           filename1_next=filename1_next, filename2_next=filename2_next)


def image_index_rendering(question_index, user_id, group_index):
    # filename = str(user_id) + '.txt'
    filename = 'group' + str(group_index) + '.txt'
    # app.logger.debug("question_index = %s", question_index)
    # app.logger.debug("filename = %s", filename)
    line = linecache.getline(filename, question_index + 1) # start from line 1!
    # app.logger.debug("line = %s", line)
    params = line.split()
    # image_index = int(params[0]) + g.user.group * SOURCE_PER_GROUP
    image_index = int(params[0])
    # app.logger.debug("image_index = %s", image_index)
    distortion_type = params[1]
    distortion_level = params[2]

    return (image_index, distortion_type, distortion_level)


@app.route('/final/', methods=['GET', 'POST'])
@login_required
def final():
    g.user = current_user
    # if g.user.s6 is False:
    if True:
        form = CommentForm(request.form)

        if form.validate_on_submit():
            comment = Comment()
            # app.logger.debug("comment = %s", comment.comment)
            form.populate_obj(comment)
            comment.user = g.user
            db.session.add(comment)

            g.user.s6 = True
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template("final.html", title="Thanks!", form=form)
    else:
        return redirect(url_for('index'))


@app.route('/create_acct/', methods=['GET', 'POST'])
def create_acct():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        group_index = group_cal()
        country = get_my_country()
        now = datetime.datetime.now()
        present_time = now.strftime("%Y-%m-%d %H:%M")

        user = User(username=form.username.data, password=form.password.data,
                    oldPassword=form.password.data, userid=(str(uuid.uuid1())),
                    image_mark_array=''.join(['0'] * SOURCE_PER_GROUP),
                    group=group_index, country=country, lastSeen=present_time)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        # # create a image display sequence for the present user
        # user_id = user.id
        # with open(os.path.join(IMAGE_FILE_ROOT, 'workfile.txt')) as f:
        #     lines = f.readlines()
        #     f.close()
        # shuffle(lines)
        # with open(os.path.join(IMAGE_FILE_ROOT, str(user_id) + '.txt'), 'w+') as g:
        #     g.writelines(lines)
        #     g.close()

        return redirect(url_for('index'))
    return render_template('create_acct.html', title="Create Account", form=form)


def group_cal():
    group_count = [0] * GROUP_NUM
    for i in range(0, GROUP_NUM):
        group_count[i] = User.query.filter(
            User.group == i, User.s5 == True).count()
        # group_count[i] = User.query.filter(User.group==i).count()

    group_index = group_count.index(min(group_count))
    # app.logger.debug("group = %s", group_count)
    # app.logger.debug("group_index = %s", group_index)
    return group_index


def get_my_country():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    # ip = str(request.remote_addr)
    # geoip = GeoIP()
    gi = pygeoip.GeoIP(os.path.join(DATABASE_ROOT, 'GeoIP.dat'))
    if ip == '127.0.0.1':
        country = "Tony"
    else:
        country = gi.country_name_by_addr(ip)
    app.logger.debug("ip = %s", ip)
    app.logger.debug("country = %s", country)
    return country


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
        user = request.form['username']
        if User.query.filter_by(username=user).first():
            q = User.query.filter_by(username=user).first()
            login_user(q)
            user = g.user
            app.logger.debug('ready to change the password')
            return redirect(request.args.get("next") or url_for("new_pass"))
        else:
            flash('Username not found', 'error')
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
    g.usermage_mark_array = ''.join(['0'] * SOURCE_PER_GROUP)
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
def delete(username):
    user = User.query.filter_by(username=username).first()
    user_id = user.id
    username = user.username
    app.logger.debug(user)
    db.session.query(Survey1).filter_by(user_id=user_id).delete()
    db.session.query(Survey2).filter_by(user_id=user_id).delete()
    db.session.query(Survey5).filter_by(user_id=user_id).delete()
    db.session.query(Comment).filter_by(user_id=user_id).delete()
    # db.session.query(Index_rendering).filter_by(user_id=user_id).delete()
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()
    # os.remove(os.path.join(IMAGE_FILE_ROOT, str(user_id) + '.txt'))
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
    if request.method == 'GET':
        users = User.query.filter_by(role=0)
        users_num = User.query.filter(User.role == 0).count()
        users_finished_num = User.query.filter(
            User.role == 0, User.s5 == True).count()

        group_count = [0] * GROUP_NUM
        for i in range(0, GROUP_NUM):
            group_count[i] = User.query.filter(
                User.group == i, User.s5 == True).count()
        if users_num == 0:
            count_per_day = [[0, 0]]
        else:
            count_per_day = day_count(users_num)
        app.logger.debug("daily count = %s", count_per_day)

        return render_template('admin/index.html', title="Admin", users=users,
                               users_num=users_num, user_finished_total=users_finished_num,
                               group_count=group_count, count_per_day=count_per_day)
    else:
        users_delete = request.form.getlist('check')
        app.logger.debug(users_delete)
        for user in users_delete:
            delete(user)
        users = User.query.filter_by(role=0)
        users_num = User.query.filter(User.role == 0).count()
        users_finished_num = User.query.filter(
            User.role == 0, User.s5 == True).count()

        group_count = [0] * GROUP_NUM
        for i in range(0, GROUP_NUM):
            group_count[i] = User.query.filter(
                User.group == i, User.s5 == True).count()
        count_per_day = day_count(users_num)
        return render_template('admin/index.html', title="Admin", users=users,
                               users_num=users_num, user_finished_total=users_finished_num,
                               group_count=group_count, count_per_day=count_per_day)


def day_count(users_num):
    timestamps_query = User.query.filter(User.role == 0).all()
    timestamps = [0] * users_num
    for i, instance in enumerate(timestamps_query):
        temp = instance.lastSeen.split(' ')
        timestamps[i] = temp[0]
    timestamps_sorted = sorted(
        timestamps, key=lambda d: map(int, d.split('-')))
    start_date = timestamps_sorted[0]
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = timestamps_sorted[-1]
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    day_num = (end_date - start_date).days + 1
    # app.logger.debug('number of days = %s', day_num)
    if day_num == 0:
        day_num = 1
    count_per_day = [[0, 0]] * day_num
    for day in range(0, day_num):
        count_per_day[day] = [day, 0]
    # app.logger.debug('count_per_day = %s', count_per_day)
    for timestamp in timestamps_sorted:
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
        if timestamp == start_date:
            day_index = 0
        else:
            day_index = (timestamp - start_date).days
        # app.logger.debug('day index = %s', day_index)
        count_per_day[day_index] = [day_index,
                                    (count_per_day[day_index][1] + 1)]
        # app.logger.debug('count_per_day = %s', count_per_day)
    return count_per_day


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
    comments = Comment.query.all()
    return render_template('admin/partials/survey2.html', title='Admin Survey-2', surveys=surveys, comments=comments)


@app.route('/admin_survey5/')
@login_required
@admin_required
def admin_survey5():
    surveys = Survey5.query.all()
    return render_template('admin/partials/survey5.html', title='Admin Survey-5', surveys=surveys)
