#Flask imports
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

#OS imports
from secrets import choice

def gen_token_url(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(token,current_app.config['SECURITY_PASSWORD_SALT'])

def gen_token(username):
    token, ascii = "", [chr(i) for i in range(65,91)]+[str(i) for i in range(10)]
    for i in range(6):
	    token += choice(ascii)
    return (username,token)

def unserialize_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        d_token = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=1800)
    except:
        d_token = False
    return d_token