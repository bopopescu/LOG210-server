from webserver.models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    
    number = Column(String(6), nullable=False)
    date = Column(DateTime, nullable=False)
    
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client")
    
    lines_order = relationship("LineOrder", cascade="save-update, merge, delete")
    
    def to_dict(self):
        my_dict = dict()

        my_dict['id'] = self.id

        return my_dict