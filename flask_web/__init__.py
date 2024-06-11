from flask import Flask
from flask_web.database.connect import session

# blueprint imports
from .home import home
from .api import api
from .datareader import SQLAlchemyAdapter
from .region import region
from .national import national
from .about import about


def create_app():
    app = Flask(__name__)

    # blueprint registration
    with app.app_context():
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(api.api_blueprint)
        app.register_blueprint(SQLAlchemyAdapter.adapter_blueprint)
        app.register_blueprint(region.regions_blueprint)
        app.register_blueprint(national.national_blueprint)
        app.register_blueprint(about.about_blueprint)

    app.config['SESSION'] = session
    app.config['SECRET_KEY'] = 'D8E767884D84F2E565D7735AA0068EDE'

    return app
