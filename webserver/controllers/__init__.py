# Function which register routes to the application
def add_routes(app):
    from webserver.controllers.countries import countries
    app.register_blueprint(countries, url_prefix='/countries')
    from webserver.controllers.restaurateurs import restaurateurs
    app.register_blueprint(restaurateurs, url_prefix='/restaurateurs')
    from webserver.controllers.restaurants import restaurants
    app.register_blueprint(restaurants, url_prefix='/restaurants')
    from webserver.controllers.clients import clients
    app.register_blueprint(clients, url_prefix='/clients')
    from webserver.controllers.entrepreneurs import entrepreneurs
    app.register_blueprint(entrepreneurs, url_prefix='/entrepreneurs')
