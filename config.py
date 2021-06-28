#Submodules
from app.API.auth import auth
from app.API.mail import mail
from app.data.models import UserModel

#Flask imports
from flask import Flask, session
from flask_login import LoginManager

#OS imports

from subprocess import run, PIPE

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

cmd = '(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Wi-Fi).IPAddress'
ip = run(["powershell","-Command",cmd], stdout = PIPE).stdout.decode("utf-8").strip()

def create_app():
    app = Flask(__name__,**init_config)
    app.config.from_object(config['development'])
    
    login_manager.init_app(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(mail)
    
    return app

@login_manager.user_loader
def load_user(username):
    user = UserModel.query(username)
    if user: 
        if user.confirmed:
            session['unconfirmed'] = False
        else:
            session['temp_user'] = user.username
            session['unconfirmed'] = True
            user = None
    return user

class BaseConfig:

    # main config
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = True
    ENV = "dev"
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = ''
    MAIL_PASSWORD = '' "platzitasks@gmail.com""Joju1116."

    # mail accounts
    MAIL_DEFAULT_SENDER = 'platzitasks@gmail.com'

class Development(BaseConfig):
    PORT = 5000
    DEBUG = True
    TESTING = False
    ENV = 'dev'

config = {
    'development': 'config.Development'
}

init_config = {
    'template_folder': "templates",
    'static_folder': "statics"
}