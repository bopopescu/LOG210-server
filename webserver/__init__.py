# Create Flask application
from flask import Flask, request, request_started
app = Flask(__name__)

# Configuration of Flask application
from webserver.config import LocalConfig
app.config.from_object(LocalConfig)

# Initialize DataBase
from webserver.config import DataBase
db = DataBase()
db.initialize(app.config['SQLALCHEMY_DATABASE_URI'])

# Add Flask route
from webserver.controllers import add_routes
add_routes(app)

@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers
    h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp

# Merge request parameters
def merge_params(sender, **extra):
    """ Function which intercept request to concat values in a same dictionary """

    if request.json is not None:
        from werkzeug.utils import CombinedMultiDict
        request.values = CombinedMultiDict([request.values, request.json])

request_started.connect(merge_params, app)