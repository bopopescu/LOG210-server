from webserver.models import Base
from sqlalchemy import Column, Integer, String

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(String(100))
    address = Column(String(100))
    city = Column(String(100))

    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['name'] = self.name
        my_dict['phone'] = self.city
        my_dict['address'] = self.address
        my_dict['city'] = self.city

        return my_dict