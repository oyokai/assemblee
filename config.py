# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://oyokai:123456@localhost/assemblee'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'