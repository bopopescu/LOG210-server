from webserver.models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class StateOrder(Base):
    __tablename__ = 'state_order'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    
    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['name'] = self.name

        return my_dict