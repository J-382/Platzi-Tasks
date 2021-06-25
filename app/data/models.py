from flask_login import UserMixin
from .database import getUserByUsername, createNewUser, activateUser

class UserModel(UserMixin):
    def __init__(self, isConfirmed, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
        self.confirmed = isConfirmed
        
    def get_id(self):
        return self.username

    @staticmethod
    def query(username):
        try:
            user_id, username, password, isConfirmed = getUserByUsername(username)
            user = UserModel(isConfirmed, user_id, username, password)
        except Exception as e:
            user = None
        return user
    
    @staticmethod
    def add(username,email,password):
        try:
            createNewUser(username,email,password)
            user = UserModel.query(username)
        except Exception as e:
            user = None
        return user

    @staticmethod
    def activate(username):
        activateUser(username)
    
    def __repr__(self) -> str:
        return "<UserModel(id={}, username={}, confirmed={})>".format(self.id, self.username, self.confirmed)


