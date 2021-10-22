from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo)
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from blogpost.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('pass_confirm', message='Password must match!')])
    pass_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.find_by_email(field.data):
            raise ValidationError('The email has been registered already')

    def validate_username(self, field):
        if User.find_by_username(field.data):
            raise ValidationError('The username has been registered already')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        modified = current_user.email != field.data
        if modified and User.find_by_email(field.data):
            raise ValidationError('The email has been registered already')

    def validate_username(self, field):
        modified = current_user.username != field.data
        if modified and User.find_by_username(field.data):
            raise ValidationError('The username has been registered already')
