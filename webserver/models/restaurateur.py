from webserver.models import Personne
from sqlalchemy import Column, Integer, String, ForeignKey

class Restaurateur(Personne):
    __tablename__ = 'restaurateur'

    id = Column(Integer, ForeignKey('personne.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'restaurateur'
    }

    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id

        return my_dict