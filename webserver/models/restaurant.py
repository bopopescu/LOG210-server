from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(100)) # !! Required !!
    phone = Column(String(100))
    cooking_type = Column(String(100))
    address = Column(String(100))
    zipcode = Column(String(100))
    city = Column(String(100))

    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country")

    restaurateur = relationship("Restaurateur", uselist=False, backref="restaurant")

    def to_dict(self, restaurateur=True):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['name'] = self.name
        my_dict['phone'] = self.phone
        my_dict['cooking_type'] = self.cooking_type
        my_dict['address'] = self.address
        my_dict['zipcode'] = self.zipcode
        my_dict['city'] = self.city

        if self.country:
            my_dict['country_id'] = self.country_id
            my_dict['country'] = self.country.to_dict()

        if self.restaurateur:
            my_dict['restaurateur_id'] = self.restaurateur.id
            if restaurateur:
                my_dict['restaurateur'] = self.restaurateur.to_dict()

        return my_dict