class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://mac:1234@db:5432/FlaskUserCRUD'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True
