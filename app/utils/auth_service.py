from app.models.user import User


def check_allowed(auth_token, role_required):
    if auth_token:
        user = User.query.filter_by(auth_token=auth_token).first()
        if user and user.role == role_required:
            return True
    return False
