from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(100)) # !! Required !!

    def to_dict(self):
        my_dict = dict()
        my_dict['id'] = self.id
        my_dict['name'] = self.name
        return my_dict