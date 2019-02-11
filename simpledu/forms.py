import re
from flask import flash
from simpledu.models import db, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired


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
