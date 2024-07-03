from flask_wtf import Form, FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from gui.user_interface.models import User


def sign_access_code():
    return 'arp0access0singularity'


class LoginForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    reset_password = SubmitField('Forgot password?')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(3, 80),
                                       Regexp('^[A-Za-z0-9_]{3,}$', message='Usernames consist of numbers, '
                                                                            'letters,and underscores.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    access_code = StringField('Access Code', validators=[DataRequired()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')

    def validate_access_code(self, access_code_field):
        if access_code_field.data != sign_access_code():
            raise ValidationError('Incorrect access code.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        user = User.query.filter_by(email=email_field.data).first()
        if user is None:
            raise ValidationError('There is no user with this email address, you must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    email = StringField(u'Email', validators=[DataRequired(), Email()])
