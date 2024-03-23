from models.question import db
from project_objects import app

# Create all database tables
with app.app_context():
    db.create_all()
