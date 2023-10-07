# function to confirm jwt validity
from functools import wraps
from flask_jwt_extended import get_jwt_identity


def checkJWTForAdmin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get("role") == "admin":
            return f(*args, **kwargs)
        else:
            return {"message": "Access Denied for Resource"}, 401
    return wrap


def checkJWTForAdminOrManager(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()

        if current_user.get("role") == "admin" or current_user.get("role") == "storeManager":
            return f(*args, **kwargs)

        else:
            return {
                "message": "Access Denied for Resource"
            }, 401
    return wrap
