from webserver.models import Personne
from sqlalchemy import Column, Integer, String, ForeignKey

class Entrepreneur(Personne):
    __tablename__ = 'entrepreneur'

    id = Column(Integer, ForeignKey('personne.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'entrepreneur'
    }

    def to_dict(self):

        my_dict = self.to_dict()
        my_dict['id'] = self.id

        return my_dict