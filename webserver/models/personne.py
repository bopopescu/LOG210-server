from webserver.models import Base
from sqlalchemy import Column, Integer, String

class Personne(Base):
    __tablename__ = 'personne'

    id = Column(Integer, primary_key=True)

    firstname = Column(String(100))
    lastname = Column(String(100))
    address = Column(String(100))
    city = Column(String(100))

    mail = Column(String(100))
    password = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'personne',
    }

    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['firstname'] = self.firstname
        my_dict['lastname'] = self.lastname
        my_dict['address'] = self.address
        my_dict['city'] = self.city
        my_dict['mail'] = self.mail

        return my_dict