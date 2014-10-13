# Create Flask application
from flask import Flask, request, request_started, g
app = Flask(__name__)

# from flask.ext.cors import CORS
# cors = CORS(app, headers="Content-Type")

# Configuration of Flask application
from webserver.config import LocalConfig
app.config.from_object(LocalConfig)

# Configuration of Flask-Babel (i18n translation)
from flask.ext.babel import Babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    return 'fr'

# Configuration of Flask-Login
from flask.ext.login import LoginManager # pip install Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize DataBase
from webserver.config import DataBase
db = DataBase()
db.initialize(app.config['SQLALCHEMY_DATABASE_URI'])

from webserver.models import Personne
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Personne).get(4)

# Add Flask route
from webserver.controllers import add_routes
add_routes(app)

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        h['Access-Control-Max-Age'] = "10"
        h['Access-Control-Allow-Credentials'] = "true"

        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp

@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Credentials'] = "true"

    return resp

def merge_params(sender, **extra):
    """ Function which intercept request to concat values in a same dictionary """

    if request.json is not None:
        from werkzeug.utils import CombinedMultiDict
        request.values = CombinedMultiDict([request.values, request.json])

request_started.connect(merge_params, app)