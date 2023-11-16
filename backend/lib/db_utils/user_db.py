from models.user import User
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from lib.db_utils.shop import ShopDB

shopDB = ShopDB()


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

    def rejectManager(self, manager_id):
        try:
            manager = User.query.get(manager_id)
            if manager and manager.role == 'unApproved':
                # TODO here I'm deleting the manager outright
                # TODO change this in future
                db.session.delete(manager)
                db.session.commit()
                return True, "Store Manager rejected"
            return False, "manager not found"
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error, flush=True)
            raise e

    def getUser(self, user_id):
        try:
            user = User.query.get(user_id)
            # TODO IF USER FOUND THEN COLLECT MORE USER DATA
            return user
        except SQLAlchemyError as e:
            return e

    def getUserData(self, user_id):
        try:
            user = self.getUser(user_id=user_id)
            if user:
                # getting all bills for user
                bills = shopDB.getBillsForUser(user_id=user_id)
                # calculating total expenditure, total saved through coupons,
                total_saved = 0
                total_expenditure = 0
                coupons_used = []
                for bill in bills:
                    # adding up the expenditure
                    total_expenditure += bill.finalAmount
                    # adding up the savings
                    savedOnBill = bill.billAmount-bill.finalAmount
                    total_saved += savedOnBill
                    coupons_used.append(bill.coupon)

            # dictionary of data
            return {
                "user": user,
                "total_saved": total_saved,
                "total_expenditure": total_expenditure,
                "coupons_used": coupons_used
            }
        except SQLAlchemyError as e:
            print(e.__dict__['orig'])
