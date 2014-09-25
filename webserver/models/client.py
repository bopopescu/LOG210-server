from webserver.models import Personne
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Client(Personne):
    __tablename__ = 'client'

    id = Column(Integer, ForeignKey('personne.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }

    def to_dict(self):

        my_dict = Personne.to_dict(self)
        my_dict['id'] = self.id

        return my_dict