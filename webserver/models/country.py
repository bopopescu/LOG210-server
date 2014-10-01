from webserver.models import Base
from sqlalchemy import Column, Integer, String

class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String(100)) # !! Required !!

    def to_dict(self):
        my_dict = dict()
        my_dict['id'] = self.id
        my_dict['name'] = self.name

        return my_dict