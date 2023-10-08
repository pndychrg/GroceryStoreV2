from models.user import User
from extensions import db
from sqlalchemy.exc import SQLAlchemyError


class UserDB:

    def checkUserExists(self, username):
        if User.query.filter_by(username=username).first():
            return True
        else:
            return False

    def registerUser(self, name, username, password, role='user'):
        if (self.checkUserExists(username=username)):
            return None, "User already exists with same name"
        # if user not exists with same username
        try:
            user = User(name=name, username=username,
                        password=password, role=role)
            db.session.add(user)
            db.session.commit()
            return user, "User Registered"
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error, flush=True)
            return None, "Database error occured"

    def loginUser(self, username, password):
        # try catch for sqlalchemy errors
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                if password == user.password:
                    return user, True
                else:
                    return "Wrong Password", False
            else:
                return "User not found with username", False
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error, flush=True)
            raise e

    def getUnapproved(self):
        # try catch for sqlalchemy errors
        try:
            unapprovedStoreManagers = User.query.filter_by(
                role='unApproved').all()
            if unapprovedStoreManagers:
                return unapprovedStoreManagers
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error, flush=True)
            raise e

    def approveManager(self, manager_id):
        try:
            manager = User.query.get(manager_id)
            if manager and manager.role == 'unApproved':
                manager.role = 'manager'
                db.session.commit()
                return True, "Store Manager Accepted"
            return False, "manager not found"
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error, flush=True)
            raise e
