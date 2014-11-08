from webserver.models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    
    number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client")
    
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship("Address")
    
    state_id = Column(Integer, ForeignKey('state_order.id'))
    state = relationship("StateOrder")
    
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship("Restaurant")
    
    lines_order = relationship("LineOrder", cascade="save-update, merge, delete")
    
    def to_dict(self, lines_order=True, state=True, address=True, restaurant=True):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['number'] = self.number
        my_dict['date'] = unicode(self.date)
        my_dict['created_date'] = unicode(self.created_date)
        my_dict['client'] = self.client.to_dict() if self.client else None
        
        if state:
            my_dict['state'] = self.state.to_dict() if self.state else None
            
        if address:
            my_dict['address'] = self.address.to_dict() if self.address else None
            
        if restaurant:
            my_dict['restaurant'] = self.restaurant.to_dict() if self.restaurant else None

        if lines_order:
            my_dict['lines_orders'] = [lo.to_dict() for lo in self.lines_order]

        return my_dict