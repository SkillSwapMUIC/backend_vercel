from flask_sqlalchemy import SQLAlchemy

from models.Category import Category

db = SQLAlchemy()


class CategoryController:
    @staticmethod
    def get_category_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def create_category(name):
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return new_category
