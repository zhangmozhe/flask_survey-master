# -*- coding: utf-8 -*-

from mixins import CRUDMixin
from flask_login import UserMixin

from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(20))
    oldPassword = db.Column(db.String(20))
    changedPass = db.Column(db.Boolean)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    group = db.Column(db.SmallInteger)
    s1 = db.Column(db.Boolean)
    s2 = db.Column(db.Boolean)
    s3 = db.Column(db.Boolean)
    s4 = db.Column(db.Boolean)
    s5 = db.Column(db.Boolean)
    s6 = db.Column(db.Boolean)
    question_index = db.Column(db.Integer)
    distortion_index_last = db.Column(db.Integer)
    distortion_index = db.Column(db.Integer)
    lastSeen = db.Column(db.String(255))
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    image_mark_array = db.Column(db.String(255))
    country = db.Column(db.String(255))


    def __init__(
            self,
            username=None,
            email=None,
            userid=None,
            password=None,
            oldPassword=None,
            changedPass=False,
            lastSeen=None,
            s1=False,
            s2=False,
            s3=False,
            s4=False,
            s5=False,
            s6=False,
            question_index=0,
            distortion_index=0,
            role=None,
            group=None,
            image_mark_array=None,
            distortion_index_last=-1,
            country=None,
            start_time=0,
            end_time=0):
        self.email = email
        self.username = username
        self.userid = userid
        self.password = password
        self.oldPassword = oldPassword
        self.changedPass = changedPass
        self.lastSeen = lastSeen
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.s5 = s5
        self.s6 = s6
        self.question_index = question_index
        self.distortion_index = distortion_index
        self.role = role
        self.group = group
        self.image_mark_array = image_mark_array
        self.distortion_index_last = distortion_index_last
        self.country = country
        self.start_time = start_time
        self.end_time = end_time

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)


# class Index_rendering(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_index = db.Column(db.String(20))
#     image_index = db.Column(db.String(20))
#     distortion_type = db.Column(db.String(255))
#     distortion_level = db.Column(db.String(20))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', uselist=False, backref='index_rendering')

#     def __init__(
#             self,
#             question_index=None,
#             image_index=None,
#             distortion_type=None,
#             distortion_level=None):
#         self.question_index = question_index
#         self.image_index = image_index
#         self.distortion_type = distortion_type
#         self.distortion_level = distortion_level

#     def get_id(self):
#         return unicode(self.id)




class Survey1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(255))
    age = db.Column(db.String(255))
    email = db.Column(db.String(20))
    experience = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey1')

    def __init__(
            self,
            gender=None,
            age=None,
            email=None,
            experience=None):
        self.gender = gender
        self.age = age
        self.email = email
        self.experience = experience

    def get_id(self):
        return unicode(self.id)


class Survey2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    understand = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey2')

    def __init__(self, understand=None):
        self.understand = understand

    def get_id(self):
        return unicode(self.id)


class Survey3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choose_names = db.Column(db.Boolean)
    choose_numbers = db.Column(db.Boolean)
    choose_songs = db.Column(db.Boolean)
    choose_mnemonic = db.Column(db.Boolean)
    choose_sports = db.Column(db.Boolean)
    choose_famous = db.Column(db.Boolean)
    choose_words = db.Column(db.Boolean)
    choose_other = db.Column(db.Boolean)
    specify = db.Column(db.String(255))
    secure_numbers = db.Column(db.Boolean)
    secure_upper_case = db.Column(db.Boolean)
    secure_symbols = db.Column(db.Boolean)
    secure_eight_chars = db.Column(db.Boolean)
    secure_no_dict = db.Column(db.Boolean)
    secure_adjacent = db.Column(db.Boolean)
    secure_nothing = db.Column(db.Boolean)
    secure_other = db.Column(db.Boolean)
    specify1 = db.Column(db.String(255))
    modify = db.Column(db.String(255))
    usedPassword = db.Column(db.String(255))
    number_N = db.Column(db.Boolean)
    number_changed_slightly = db.Column(db.Boolean)
    number_changed_completely = db.Column(db.Boolean)
    number_added_digits = db.Column(db.Boolean)
    number_deleted_digits = db.Column(db.Boolean)
    number_substituted_digits = db.Column(db.Boolean)
    number_O = db.Column(db.String(255))
    char_N = db.Column(db.Boolean)
    char_changed_slightly = db.Column(db.Boolean)
    char_changed_completly = db.Column(db.Boolean)
    char_added_symbols = db.Column(db.Boolean)
    char_deleted_symbols = db.Column(db.Boolean)
    char_substituted_symbols = db.Column(db.Boolean)
    not_changed1 = db.Column(db.Boolean)
    changed_slightly1 = db.Column(db.Boolean)
    changed_completly1 = db.Column(db.Boolean)
    capatalized1 = db.Column(db.Boolean)
    addedwords = db.Column(db.Boolean)
    deletedwords = db.Column(db.Boolean)
    char_O = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey3')

    def __init__(
            self,
            choose_names=None,
            choose_numbers=None,
            choose_songs=None,
            choose_mnemonic=None,
            choose_sports=None,
            choose_famous=None,
            choose_words=None,
            secure_numbers=None,
            secure_upper_case=None,
            secure_symbols=None,
            secure_eight_chars=None,
            secure_no_dict=None,
            secure_adjacent=None,
            secure_nothing=None,
            modify=None,
            usedPassword=None,
            number_N=None,
            number_added_digits=None,
            number_deleted_digits=None,
            number_substituted_digits=None,
            number_O=None,
            char_N=None,
            char_added_symbols=None,
            char_deleted_symbols=None,
            char_substituted_symbols=None,
            char_O=None,
            userid=None,
            choose_other=None,
            specify=None,
            specify1=None,
            secure_other=None,
            number_changed_completly=None,
            number_changed_slightly=None,
            char_changed_slightly=None,
            char_changed_completly=None,
            not_changed1=None,
            changed_completly1=None,
            changed_slightly1=None,
            capatalized1=None,
            addedwords=None,
            deletedwords=None):

        self.choose_names = choose_names
        self.choose_numbers = choose_numbers
        self.choose_songs = choose_songs
        self.choose_mnemonic = choose_mnemonic
        self.choose_sports = choose_sports
        self.choose_famous = choose_famous
        self.choose_words = choose_words
        self.choose_other = choose_other
        self.specify = specify
        self.secure_numbers = secure_numbers
        self.secure_upper_case = secure_upper_case
        self.secure_symbols = secure_symbols
        self.secure_eight_chars = secure_eight_chars
        self.secure_no_dict = secure_no_dict
        self.secure_adjacent = secure_adjacent
        self.secure_nothing = secure_nothing
        self.secure_other = secure_other
        self.specify1 = specify1
        self.modify = modify
        self.usedPassword = usedPassword
        self.not_changed1 = not_changed1
        self.changed_slightly1 = changed_slightly1
        self.changed_completly1 = changed_completly1
        self.capatalized1 = capatalized1
        self.addedwords = addedwords
        self.deletedwords = deletedwords
        self.number_N = number_N
        self.number_changed_slightly = number_changed_slightly
        self.number_changed_completly = number_changed_completly
        self.number_added_digits = number_added_digits
        self.number_deleted_digits = number_deleted_digits
        self.number_substituted_digits = number_substituted_digits
        self.number_O = number_O
        self.char_N = char_N
        self.char_changed_slightly = char_changed_slightly
        self.char_changed_completly = char_changed_completly
        self.char_added_symbols = char_added_symbols
        self.char_deleted_symbols = char_deleted_symbols
        self.char_substituted_symbols = char_substituted_symbols
        self.char_O = char_O
        self.userid = userid

    def get_id(self):
        return unicode(self.id)


class Survey4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    computerTime = db.Column(db.String(255))
    pass_random = db.Column(db.Boolean)
    pass_reuse = db.Column(db.Boolean)
    pass_modify = db.Column(db.Boolean)
    pass_new = db.Column(db.Boolean)
    pass_substitute = db.Column(db.Boolean)
    pass_multiword = db.Column(db.Boolean)
    pass_phrase = db.Column(db.Boolean)
    pass_O = db.Column(db.String(255))
    how_regular_file = db.Column(db.Boolean)
    how_encrypted = db.Column(db.Boolean)
    how_software = db.Column(db.Boolean)
    how_cellphone = db.Column(db.Boolean)
    how_browser = db.Column(db.Boolean)
    how_write_down = db.Column(db.Boolean)
    how_no = db.Column(db.Boolean)
    comments = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey4')

    def __init__(
            self,
            computerTime=None,
            pass_random=None,
            pass_reuse=None,
            pass_modify=None,
            pass_new=None,
            pass_substitute=None,
            pass_multiword=None,
            pass_phrase=None,
            pass_O=None,
            how_regular_file=None,
            how_encrypted=None,
            how_software=None,
            how_cellphone=None,
            how_browser=None,
            how_write_down=None,
            how_no=None,
            comments=None,
            userid=None):

        self.computerTime = computerTime
        self.pass_random = pass_random
        self.pass_reuse = pass_reuse
        self.pass_modify = pass_modify
        self.pass_new = pass_new
        self.pass_substitute = pass_substitute
        self.pass_multiword = pass_multiword
        self.pass_phrase = pass_phrase
        self.pass_O = pass_O
        self.how_regular_file = how_regular_file
        self.how_encrypted = how_encrypted
        self.how_software = how_software
        self.how_cellphone = how_cellphone
        self.how_browser = how_browser
        self.how_write_down = how_write_down
        self.how_no = how_no
        self.comments = comments
        self.userid = userid

    def get_id(self):
        return unicode(self.id)



class Survey5(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distortion = db.Column(db.String(255))
    coverage = db.Column(db.String(255))
    total_marks = db.Column(db.String(255))
    question_index = db.Column(db.Integer)
    image_index = db.Column(db.Integer)
    distortion_type = db.Column(db.String(255))
    distortion_level = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey5')

    def __init__(
            self,
            distortion=None,
            coverage=None,
            total_marks=None,
            image_index=None,
            distortion_type=None,
            distortion_level=None,
            question_index=None):
        self.distortion = distortion
        self.coverage = coverage
        self.total_marks = total_marks
        self.question_index = question_index
        self.image_index = image_index
        self.distortion_type = distortion_type
        self.distortion_level = distortion_level

    def get_id(self):
        return unicode(self.id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='comment')

    def __init__(
            self,
            comment=None):
        self.comment = comment

    def get_id(self):
        return unicode(self.id)