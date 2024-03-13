from flask_sqlalchemy import SQLAlchemy

from .AnswerPost import AnswerPost
from .Category import Category
from .Course import Course
from .QuestionPost import QuestionPost
from .Section import Section
from .User import User
from .VisitedCourse import VisitedCourse

# Initialize the SQLAlchemy object
db = SQLAlchemy()
