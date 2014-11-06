from webserver.models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    
    number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    created = Column(DateTime, default=datetime.now)
    
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client")
    
    state_id = Column(Integer, ForeignKey('state_order.id'))
    state = relationship("StateOrder")
    
    lines_order = relationship("LineOrder", cascade="save-update, merge, delete")
    
    def to_dict(self, lines_order=True):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['number'] = self.number
        my_dict['date'] = unicode(self.date)
        my_dict['created'] = unicode(self.created)
        my_dict['client'] = self.client.to_dict() if self.client else None
        my_dict['state'] = self.state.to_dict() if self.state else None

        if lines_order:
            my_dict['lines_orders'] = [so.to_dict() for so in self.lines_order]

        return my_dict