import os

from flask import Flask

from app.db import db


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_KEY")

    ############## Fixing the security, but it did not work ################
    # pg_user = os.environ.get("PG_USER")
    # password = os.environ.get("PG_PASSWORD")
    # app.config["SQLALCHEMY_DATABASE_URI"] = (
    # f"postgresql://{pg_user}:{password}@dpg"
    # "-co7cesf79t8c73a3pr00-a.singapore-postgres.render.com/remote_pg_db_pr3l"
    # )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://root:biqHV5nNSu1OeaBcp4Vwyg6DTqihKJ9D@dpg"
        "-co7cesf79t8c73a3pr00-a.singapore-postgres.render.com/remote_pg_db_pr3l"
    )

    db.init_app(app)
    with app.app_context():
        # Importing models here ensures they are properly registered with SQLAlchemy
        from app.models import course  # noqa
        from app.models import post_qanda  # noqa
        from app.models import question  # noqa
        from app.models import user  # noqa

        # Create database tables if they don't exist
        db.create_all()

        from app.routes.auth import auth_route
        from app.routes.course import course_route
        from app.routes.home import home_route
        from app.routes.qanda import qanda_route
        from app.routes.search import search_route

        app.register_blueprint(home_route, url_prefix="/")
        app.register_blueprint(qanda_route, url_prefix="/qanda")
        app.register_blueprint(course_route, url_prefix="/course")
        app.register_blueprint(search_route, url_prefix="/search")
        app.register_blueprint(auth_route, url_prefix="/auth")

        # Dropping the "post" table
        # from sqlalchemy import MetaData, Table, create_engine, exc
        # meta = MetaData()
        # meta.reflect(bind=db.engine)
        # try:
        #     post_table = Table('post', meta, autoload=True, autoload_with=db.engine)
        #     post_table.drop(db.engine)
        # except exc.NoSuchTableError:
        #     print("Table 'post' does not exist.")

        return app
