# app/config.py

class Config:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2401658158@localhost/managerSystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
