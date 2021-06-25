from sqlalchemy import create_engine,\
     Boolean, DateTime, Column, Integer, String, ForeignKey,\
     insert, select, update
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash as gen_pass
from subprocess import run, PIPE

ip = run(["powershell","-Command",'(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Wi-Fi).IPAddress']\
    , stdout = PIPE).stdout.decode("utf-8").strip()

engine = create_engine('postgresql://postgres:password@{}:3000/postgres'.format(ip))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True,nullable=False)
    email = Column(String(30),unique=True,nullable=False)
    password = Column(String(1000),nullable=False)
    confirmed = Column(Boolean,nullable=False,default=0)
    confirmed_on = Column(DateTime)
    tasks = relationship("Task")

    def __repr__(self) -> str:
        return "<User(username={}, email={}, confirmed={}, confirmed_on={})".format(\
            self.username, self.email, self.confirmed, self.confirmed_on)
    

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True} 

    taks_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(50), nullable=False)
    description = Column(String(1000))
    finished = Column(Boolean, default=False)
    start_on = Column(DateTime, default=now())
    important = Column(Integer, default=0)
    CheckConstraint('important <= 5 AND important >= 0')

    def __repr__(self) -> str:
        return "<Test(user_id={}, description={}, finished={}, start_on)".format(\
            self.username, self.email, self.confirmed, self.confirmed_on)

Base.metadata.create_all(engine)

def getUserByUsername(username):
    return session.query(User.user_id, User.username, User.password, User.confirmed).\
        filter(User.username == username).first()

def createNewUser(username,email,password):
    hashed_password = gen_pass(password)
    new_user = User(username=username,email=email,password=hashed_password)
    try:
        session.add(new_user)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise Exception(e.orig)

def activateUser(username):
    try:
        session.query(User)\
        .filter(User.username == username)\
        .update({User.confirmed: True, User.confirmed_on: now()})
        session.commit()
    except IntegrityError as e:
        raise Exception(e.orig)

def getTaskByUserID(user_id):
    return session.query(Task.name, Task.description, Task.finished, Task.start_on, Task.important).\
        filter(Task.user_id == user_id).all()