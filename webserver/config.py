from webserver.models import Base

__all__ = ['DataBase', 'LocalConfig', 'TestingConfig']

class DataBase(object):

    def __init__(self):

        # Initialize null session
        self._session = None

    def initialize(self, db_path):

        # Define engine SQLAlchemy
        from sqlalchemy import create_engine
        engine = create_engine(db_path)
        self._engine = engine

        # Create session
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self._session = Session()

    def create_all(self):

        # Create database
        Base.metadata.create_all(self._engine)

    def drop_all(self):

        # Delete database
        Base.metadata.drop_all(self._engine)

    def _get_engine(self):

        # Return engine
        return self._engine

    def _get_session(self):

        # Return current session
        return self._session

    engine = property(_get_engine, None, None)
    session = property(_get_session, None, None)


class LocalConfig(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'foobarbaz'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:8889/restaurants'


class TestingConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class TwilioConfig(object):
    ACCOUNT_SID = "AC46b7911c51e43edf923538fa46829be8" 
    AUTH_TOKEN = "742c842bb3002878ba2d374b2baf54ea"