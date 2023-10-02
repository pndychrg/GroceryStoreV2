from models.roles import Role
from models.user import User
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

class UserDB:

    def checkUserExists(self,username):
        if User.query.filter_by(username=username).first():
            return True
        else:
            return False

    def registerUser(self,name,username,password):
        if(self.checkUserExists(username=username)):
            return None
        
        # if user not exists with same username
        try:
            user = User(name=name,username=username,password=password)
            print(user.roles,flush=True)
            # adding the user role to this user
            role = Role.query.filter_by(name="user").first()
            if role != None:
                user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error,flush=True)
            raise e
        
    def loginUser(self,username,password):
        
        # try catch for sqlalchemy errors
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                if password == user.password :
                    return user,True
                else :
                    return "Wrong Password",False
            else:
                return "User not found with username",False
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error,flush=True)
            raise e