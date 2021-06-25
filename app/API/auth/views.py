#Submodules
from flask_login.utils import login_user
from . import auth
from ..forms import LoginForm, SignUpForm
from .authentication import login as try_login
from .authentication import sign_up as try_signup
from .authentication import AuthException

#mail module
from ..mail import mail_confirmation_redirect

#Flask imports
from flask import render_template, make_response, redirect, session
from flask.helpers import flash, url_for
from flask_login import current_user


@auth.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    response = render_template("login.html", **context)
    if login_form.validate_on_submit():
        try:
            try_login(login_form.username.data,login_form.password.data)
            print(current_user)
            response = make_response(redirect(url_for("main_app")))
        except AuthException as e:
            flash(e.message,"error")
            response = make_response(redirect("login"))
    return response


@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    signup_form = SignUpForm()
    context = {
        'signup_form': signup_form
    }
    response = render_template("sign_up.html", **context)
    if signup_form.validate_on_submit():
        try:
            print(signup_form.username.data)
            try_signup(signup_form.username.data, signup_form.mail.data, signup_form.password.data)
            response = make_response(redirect(mail_confirmation_redirect(signup_form.username.data)))
            flash("We have sent you an email to activate your account :)","message")
        except AuthException as e:
            flash(e.message,"error")
            response = make_response(redirect("signup"))
        except Exception as e:
            print(e)
    return response
