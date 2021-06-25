from app.API.mail.token import gen_token_url
from flask import Blueprint

mail = Blueprint('mail',__name__ ,url_prefix='/mail')

from . import views 
from .views import mail_confirmation_redirect