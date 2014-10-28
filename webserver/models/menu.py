from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    dishes = relationship("Dish", cascade="save-update, merge, delete")
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    
    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['name'] = self.name
        my_dict['dishes'] = [dish.to_dict() for dish in self.dishes] if self.dishes else []

        return my_dict