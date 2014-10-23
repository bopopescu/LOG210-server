from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False) # !! Required !!
    description = Column(String(255), nullable=False) # !! Required !!
    price = Column(Float, nullable=False) # !! Required !!


    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['name'] = self.name
        my_dict['description'] = self.description
        my_dict['price'] = self.price

        return my_dict