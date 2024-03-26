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

        return app


app = create_app()
