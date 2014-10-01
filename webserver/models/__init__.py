# Declarative base to create models
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Export Models
__all__ = ['Country', 'Personne', 'Entrepreneur', 'Client', 'Restaurateur', 'Restaurant']


from webserver.models.country import Country
from webserver.models.personne import Personne
from webserver.models.entrepreneur import Entrepreneur
from webserver.models.client import Client
from webserver.models.restaurant import Restaurant
from webserver.models.restaurateur import Restaurateur