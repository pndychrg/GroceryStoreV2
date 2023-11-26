import base64
from models.user import User
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from lib.db_utils.shop import ShopDB
from lib.db_utils.rating import RatingMethods
from datetime import datetime

shopDB = ShopDB()
ratingDB = RatingMethods()


class UserDB:

    def checkUserExists(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    def registerUser(self, name, username, email, password, role='user'):
        if (self.checkUserExists(username=username)):
            return None, "User already exists with same name"
        # if user not exists with same username
        try:
            user = User(name=name, username=username,
                        password=password, role=role, email=email)
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
            print(e)
            return None

    def getPreviousMonthUserData(self, user_id):
        try:
            user = self.getUser(user_id=user_id)
            if user:
                # getting all bills for user
                bills, month = shopDB.getPreviousMonthBillsForUser(
                    user_id=user_id)
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
                    if bill.coupon:
                        coupons_used.append(bill.coupon)

            # dictionary of data
            return {
                "user": user,
                "total_saved": total_saved,
                "ratings": [rating.toJson() for rating in user.ratings],
                "bills": bills,
                "total_expenditure": total_expenditure,
                "coupons_used": coupons_used,
                "month": month
            }
        except SQLAlchemyError as e:
            print(e.__dict__['orig'])

    def getUserCurrentMonthData(self, user_id):
        try:
            user = self.getUser(user_id=user_id)
            if user:
                today = datetime.today()
                # getting all bills for user
                bills = shopDB.getCurrentMonthBillsForUser(user_id=user_id)
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
                    if bill.coupon:
                        coupons_used.append(bill.coupon)
            # generating the img_string earlier
            image = base64.b64encode(user.img).decode(
                'utf-8') if user.img != None else None
            # print(str(image))
            # dictionary of data
            return {
                "user": user,
                "img": "data:image/png;base64,"+image,
                "ratings": [rating.toJson() for rating in user.ratings],
                "total_saved": total_saved,
                "bills": bills,
                "total_expenditure": total_expenditure,
                "coupons_used": coupons_used,
                "month": today.strftime("%B %Y")
            }
        except SQLAlchemyError as e:
            print(e.__dict__['orig'])

    def getAllUser(self):
        users = User.query.filter_by(role="user").all()
        return users

    def setUserImage(self, user_id, image):
        # getting the user from user_id
        user = self.getUser(user_id=user_id)
        if user:
            user.img = image
            db.session.commit()
            return user, "User Data Updated"

        else:
            return None, "User not found"

    def updateUser(self, user_id, name, username, email, password):
        # getting the from user_id
        user = self.getUser(user_id=user_id)
        # print(img, flush=True)
        # check if another user already exists with same username
        if user:
            # first checking if the password is correct or not
            print(password, user.password, flush=True)
            if password != user.password:
                return None, "incorrect password"
            existingUser = self.checkUserExists(username=username)
            if existingUser.id != user.id:
                return None, "username already in use"
            # update the user
            user.name = name
            user.username = username
            # user.img = img
            user.email = email
            db.session.commit()
            return user, "user updated"
        else:
            return None, "invalid user_id"
