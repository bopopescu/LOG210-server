from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flaskext.auth.auth import AuthUser

class Personne(Base):
    __tablename__ = 'personne'

    id = Column(Integer, primary_key=True)

    firstname = Column(String(100)) # Required
    lastname = Column(String(100))  # Required
    phone = Column(String(100))
    address = Column(String(100))
    zipcode = Column(String(100))
    city = Column(String(100))
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country")

    mail = Column(String(100))      # Required
    password = Column(String(100))  # Required

    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'personne',
        'polymorphic_on': type
    }

    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['firstname'] = self.firstname
        my_dict['lastname'] = self.lastname
        my_dict['phone'] = self.phone
        my_dict['address'] = self.address
        my_dict['zipcode'] = self.zipcode
        my_dict['city'] = self.city

        if self.country:
            my_dict['country_id'] = self.country_id
            my_dict['country'] = self.country.to_dict()

        my_dict['mail'] = self.mail
        my_dict['password'] = self.password

        my_dict['type'] = self.type

        return my_dict
