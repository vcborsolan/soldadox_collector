from flask import Flask
from flask_migrate import Migrate
from .model import configure as config_db
from .serealizer import configure as config_ma
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from .soldadox import bp_soldadox


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://admin:admin@localhost:54320/default_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False
    config_db(app)
    config_ma(app)
    sentry_sdk.init(dsn="https://225751dc0e8e4a2095a83abccc18b3f0@o415817.ingest.sentry.io/5307474",integrations=[FlaskIntegration()])

    Migrate(app , app.db)

    app.register_blueprint(bp_soldadox)

    return app

app = create_app()