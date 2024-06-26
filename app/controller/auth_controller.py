import hashlib

from app import db
from app.models.post_qanda import Post
from app.models.user import User


def login_user(email, password, role):
    user = User.query.filter_by(email=email).first()

    if not user:
        # generate auth_token from email and password, by hashing the string "email:password"
        auth_token = str(email + ":" + password)
        auth_token = hashlib.sha256(auth_token.encode()).hexdigest()

        user = User(email=email, password=password, auth_token=auth_token, role=role)
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


def user_allowed_to_edit_post(auth_token, post_id):
    post = Post.query.filter_by(id=post_id).first()

    if auth_token == post.creator:
        return True
    else:
        return False


def check_allowed(auth_token, role_required):
    if auth_token:
        user = User.query.filter_by(auth_token=auth_token).first()
        if user and user.role == role_required:
            return True
    return False
