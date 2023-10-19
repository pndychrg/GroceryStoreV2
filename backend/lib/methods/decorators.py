# function to confirm jwt validity
from functools import wraps
from flask_jwt_extended import get_jwt_identity


def checkJWTForAdmin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user.get('role'), flush=True)
        if current_user.get("role") == "admin":
            return f(*args, **kwargs)
        else:
            return {"msg": "Access Denied for Resource"}, 401
    return wrap


def checkJWTForAdminOrManager(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()

        if current_user.get("role") == "admin" or current_user.get("role") == "manager":
            return f(*args, **kwargs)

        else:
            return {
                "msg": "Access Denied for Resource"
            }, 401
    return wrap


def checkJWTForManager(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()

        if current_user.get("role") == 'manager':
            return f(*args, **kwargs)

        else:
            return {
                'msg': 'Access Denied for Resource'
            }, 401
    return wrap


def checkJWTForUser(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get("role") == 'user':
            return f(*args, **kwargs)

        else:
            return {
                'msg': 'Access Denied for Resource'
            }, 401
    return wrap


def checkJWTForUserOrManager(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get('role') == 'user' or current_user.get('role') == 'manager':
            return f(*args, **kwargs)

        else:
            return {
                'msg': "Access Denied for Resource"
            }, 401

    return wrap
