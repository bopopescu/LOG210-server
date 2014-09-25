from webserver.models import Personne
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Restaurateur(Personne):
    __tablename__ = 'restaurateur'

    id = Column(Integer, ForeignKey('personne.id'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'restaurateur'
    }

    def to_dict(self):

        my_dict = Personne.to_dict(self)
        my_dict['id'] = self.id
        my_dict['restaurant_id'] = self.restaurant_id

        if self.restaurant:
            my_dict['restaurant'] = self.restaurant.to_dict(False)

        return my_dict