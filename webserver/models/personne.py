from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flaskext.auth.auth import AuthUser
from flask.ext.login import UserMixin

class Personne(Base):
    __tablename__ = 'personne'

    id = Column(Integer, primary_key=True)

    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    birthdate = Column(DateTime)
    phone = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    zipcode = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country")
    language = Column(String(100), nullable=False, default="fr")

    mail = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'personne',
        'polymorphic_on': type
    }

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['firstname'] = self.firstname
        my_dict['lastname'] = self.lastname
        my_dict['birthdate'] = unicode(self.birthdate) if self.birthdate else None
        my_dict['phone'] = self.phone
        my_dict['address'] = self.address
        my_dict['zipcode'] = self.zipcode
        my_dict['city'] = self.city
        my_dict['language'] = self.language

        if self.country:
            my_dict['country_id'] = self.country_id
            my_dict['country'] = self.country.to_dict()

        my_dict['mail'] = self.mail
        my_dict['password'] = self.password

        my_dict['type'] = self.type

        return my_dict
