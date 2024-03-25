from flask import Flask

from .db import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        # Importing models here ensures they are properly registered with SQLAlchemy
        from app.models import question  # noqa

        # Create database tables if they don't exist
        db.create_all()

        # Importing routes here ensures they are registered with the application
        from app.routes.routes import home_route

        app.register_blueprint(home_route)
        return app


app = create_app()
