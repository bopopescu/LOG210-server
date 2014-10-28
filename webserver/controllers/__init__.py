# Function which register routes to the application
def add_routes(app):
    from webserver.controllers.accesstokens import accesstokens
    app.register_blueprint(accesstokens, url_prefix='/accesstokens')
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
    from webserver.controllers.livreurs import livreurs
    app.register_blueprint(livreurs, url_prefix='/livreurs')
    from webserver.controllers.dishes import dishes
    app.register_blueprint(dishes, url_prefix='/dishes')
    from webserver.controllers.menus_dishes import menus_dishes
    app.register_blueprint(menus_dishes, url_prefix='/menus')
    from webserver.controllers.menus import menus
    app.register_blueprint(menus, url_prefix='/menus')
    from webserver.controllers.orders import orders
    app.register_blueprint(orders, url_prefix='/orders')
    from webserver.controllers.states_orders import states_orders
    app.register_blueprint(states_orders, url_prefix='/orders/states')
    

