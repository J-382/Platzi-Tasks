#Submodules
from app.data.models import UserModel
from . import mail
from .token import gen_token, gen_token_url, unserialize_token
from ..forms import ConfirmForm

#Flask imports
from flask import current_app, make_response, session, render_template, url_for, redirect, request, flash
from flask_mail import Message, Mail

def mail_confirmation_redirect(username):
    mail_manager = Mail(current_app)
    token = gen_token(username)
    token_url = url_for('mail.confirm_token', token=gen_token_url(token))
    msg = Message("Hello there!",\
                    sender=current_app.config["MAIL_DEFAULT_SENDER"],recipients=["jrperezdeleon@gmail.com"])
    msg.html = render_template("mail.html",token=token)
    mail_manager.send(msg)
    return token_url

@mail.route("/confirm/<token>", methods=['GET', 'POST'])
def confirm_token(token):
    confirm_form = ConfirmForm()
    context = {
        'url': 'www.google.com',
        'confirm_form': confirm_form
    }
    unserialized = unserialize_token(token)
    response = render_template('confirm.html',**context)
    if unserialized:
        print(session.get('unconfirmed'),session.get('temp_user'))
        if session.get('unconfirmed') and session.get('temp_user') == unserialized[0] and confirm_form.validate_on_submit():
            if confirm_form.token.data == unserialized[1]:
                UserModel.activate(session.get('temp_user'))
                flash("your account was activated successfully")
                response = make_response(redirect(url_for("main_app")))
                session.pop('temp_user')
            else:
                flash("Invalid Token","error")
                response = make_response(redirect(request.url))
    else:
        flash("Token expired", "error")
        response = make_response(redirect(url_for("auth.sign_up")))

    return response