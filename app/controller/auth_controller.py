import hashlib

from app import db
from app.models.user import User


def login_user(email, password, role):
    user = User.query.filter_by(email=email).first()

    if not user:
        # generate auth_token from email and password, by hashing the string "email:password"
        auth_token = str(email + ":" + password)
        auth_token = hashlib.sha256(auth_token.encode()).hexdigest()

        user = User(email=email, password=password, auth_token=auth_token, role=role)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        print("logged in with auth_token: " + str(auth_token))
        return True, auth_token
    elif user.check_password(password):
        auth_token = user.auth_token
        print(auth_token)
        return True, auth_token
    else:
        return False, None


def is_teacher(auth_token):
    try:
        user = User.query.filter_by(auth_token=auth_token).first()
        if user.role == "teacher":
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
