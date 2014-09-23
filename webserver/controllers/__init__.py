# Function which register routes to the application
def add_routes(app):
    from webserver.controllers.restaurateurs import restaurateurs
    app.register_blueprint(restaurateurs, url_prefix='/restaurateurs')
    from webserver.controllers.restaurants import restaurants
    app.register_blueprint(restaurants, url_prefix='/restaurants')
    from webserver.controllers.roles import roles
    app.register_blueprint(roles, url_prefix='/roles')
