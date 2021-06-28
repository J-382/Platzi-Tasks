#Submodules
from app.data.models import UserModel

#Flask imports
from flask import make_response, url_for, request, redirect
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash as check_pass

#OS imports
from functools import wraps

class AuthException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)

def login(username,password):
    user = UserModel.query(username)
    print(user)
    if user == None:
        raise AuthException("User not exists")
    elif user.confirmed:
        if check_pass(user.password,password):
            login_user(user)
        else:
            raise AuthException("Wrong username or password") 
    else:
        raise AuthException("User is not activated")

def sign_up(username,email,password):
    try:
        new_user = UserModel.add(username,email,password)
        login_user(new_user)
    except:
        raise AuthException("User already exists")
