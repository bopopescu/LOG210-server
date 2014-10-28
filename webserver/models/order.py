from webserver.models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    
    number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client")
    
    state_id = Column(Integer, ForeignKey('state_order.id'))
    state = relationship("StateOrder")
    
    lines_order = relationship("LineOrder", cascade="save-update, merge, delete")
    
    def to_dict(self, dishes=True):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['number'] = self.number
        my_dict['date'] = unicode(self.date)
        my_dict['client'] = self.client.to_dict() if self.client else None

        if dishes:
            my_dict['lines_orders'] = [{'dish': so.dish.to_dict(), 'quantity': so.quantity} for so in self.lines_order]

        return my_dict