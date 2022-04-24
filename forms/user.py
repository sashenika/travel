from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname')
    name = StringField('Name')
    age = IntegerField('Age')
    town = StringField('Town')

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')