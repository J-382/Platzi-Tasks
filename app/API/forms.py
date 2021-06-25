from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log in")

class SignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    mail = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class ConfirmForm(FlaskForm):
    token = StringField('Token',validators=[DataRequired()])
    submit = SubmitField("Active my account")