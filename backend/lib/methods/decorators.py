# function to confirm jwt validity
from functools import wraps
from flask_jwt_extended import get_jwt_identity


def checkJWTForAdmin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get("role") != "user":
            return f(*args, **kwargs)
        else:
            return {"message": "Access Denied for Resource"}, 401
    return wrap
