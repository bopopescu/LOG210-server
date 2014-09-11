# Declarative base to create models
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Export Models
__all__ = ['Personne', 'Restaurateur', 'Restaurant']
from webserver.models.personne import Personne
from webserver.models.restaurant import Restaurant
from webserver.models.restaurateur import Restaurateur