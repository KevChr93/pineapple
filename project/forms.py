from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,Form, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from project import db

class subForm(FlaskForm):
    plan = SelectField('Subscription Plan', choices=[('FREE', 'Free'), ('PRO.', 'Professional'), ('ENTERPRISE', 'Enterprise')])
    submit = SubmitField('Sign Up')

class RegForm(FlaskForm):
    firstname = StringField('FirstName',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('LastName',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validateUsername(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise validationError('Username is already taken')

    def validatEmail(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise validationError('email is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')