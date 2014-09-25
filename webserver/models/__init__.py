# Declarative base to create models
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Export Models
__all__ = ['Personne', 'Entrepreneur', 'Client', 'Restaurateur', 'Restaurant']


from webserver.models.personne import Personne
from webserver.models.entrepreneur import Entrepreneur
from webserver.models.client import Client
from webserver.models.restaurant import Restaurant
from webserver.models.restaurateur import Restaurateur