from flask import Flask
from flask_session import Session

from app.db import db


def create_app():
    app = Flask(__name__)
    app.secret_key = (
        "iauhfiebndfciqbdfiuqbfiaqubfcnpuBDFCUQZEBFUQ"  # Change this to your secret key
    )

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://sql6694920:hkMeVmh7Sc@sql6.freemysqlhosting.net:3306/sql6694920"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_TYPE"] = "sqlalchemy"

    db.init_app(app)

    app.config["SESSION_SQLALCHEMY"] = db
    app.config["SESSION_COOKIE_NAME"] = "session_of_skillswap"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_KEY_PREFIX"] = "SESSION"

    Session(app)

    with app.app_context():
        # Importing models here ensures they are properly registered with SQLAlchemy
        from app.models import course  # noqa
        from app.models import question  # noqa
        from app.models import user  # noqa

        # Create database tables if they don't exist
        db.create_all()

        from app.routes.auth import auth_route
        from app.routes.course import course_route
        from app.routes.home import home_route
        from app.routes.qanda import qanda_route
        from app.routes.search import search_route
        from app.routes.user import user_route

        app.register_blueprint(home_route, url_prefix="/")
        app.register_blueprint(qanda_route, url_prefix="/qanda")
        app.register_blueprint(user_route, url_prefix="/user")
        app.register_blueprint(course_route, url_prefix="/course")
        app.register_blueprint(search_route, url_prefix="/search")
        app.register_blueprint(auth_route, url_prefix="/auth")

        return app
