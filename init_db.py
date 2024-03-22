from index import app, db

# Create all database tables
with app.app_context():
    db.create_all()
