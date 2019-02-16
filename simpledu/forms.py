import re
from flask import flash
from simpledu.models import db, User, Course
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入正确的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6-24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='密码不一致')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user
    
    def validate_username(self, field):
        temp = len(re.findall('[a-zA-Z_0-9]', field.data))
        if temp != len(field.data):
            flash('用户名只能使用字母和数字','warning')
        elif User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已经存在')
        

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username(self, field):
        temp = len(re.findall('[a-zA-Z_0-9]', field.data))
        if temp != len(field.data):
            flash('用户名只能使用字母和数字','warning')
        elif not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名未注册')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[DataRequired(), Length(20,256)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输>入正确的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6-24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='密码不一致')])
    role = IntegerField('权限', validators=[DataRequired()])
    job = StringField('职业', validators=[DataRequired(), Length(3, 24)])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    
    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        temp = len(re.findall('[a-zA-Z_0-9]', field.data))
        if temp != len(field.data):
            flash('用户名只能使用字母和数字','warning')
        elif User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已经存在')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def validate_role(self, field):
        if field.data not in [User.ROLE_USER, User.ROLE_STAFF, User.ROLE_ADMIN]:
            raise ValidationError('权限设置错误')
