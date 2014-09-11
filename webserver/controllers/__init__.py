# Function which register routes to the application
def add_routes(app):
    from webserver.controllers.restaurants import restaurants
    app.register_blueprint(restaurants, url_prefix='/restaurants')