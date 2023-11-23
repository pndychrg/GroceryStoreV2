from sqlalchemy import extract
from models.bill import Bill
from models.order import Order
from lib.methods.validators import Validators
from lib.db_utils.cart import CartDB
from lib.db_utils.coupons import CouponDB
from datetime import datetime, timedelta
from extensions import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# init
validators = Validators()
cartDB = CartDB()
couponDB = CouponDB()


class ShopDB:

    def getBillsForUser(self, user_id):
        bills = Bill.query.filter_by(user_id=user_id).all()
        return bills

    def getPreviousMonthBillsForUser(self, user_id):
        # calculating the start and end dates for the previous month
        today = datetime.now()
        first_dayofcurrentmonth = today.replace(day=1)
        last_dayofpreviousmonth = first_dayofcurrentmonth - timedelta(days=1)
        first_dayofpreviousmonth = last_dayofpreviousmonth.replace(day=1)

        # now quering
        bills = Bill.query.filter(Bill.user_id == user_id, extract(
            'year', Bill.date) == last_dayofpreviousmonth.year, extract('month', Bill.date) == last_dayofpreviousmonth.month)

        return bills, first_dayofpreviousmonth.strftime("%B %Y")

    def getCurrentMonthBillsForUser(self, user_id):
        today = datetime.now()
        bills = Bill.query.filter(Bill.user_id == user_id,
                                  extract('year', Bill.date) == today.year, extract(
                                      'month', Bill.date) == today.month
                                  )
        return bills

    def buy(self, user_id, coupon_id=None):

        # getting the cart for user and cart sum
        unboughtCartFor_user, cartSum = cartDB.getCartProducts(user_id=user_id)

        # checking if cart is not empty
        if len(unboughtCartFor_user) > 0:
            # checking if the products in cart are available at the current moment or not

            for cartEntry in unboughtCartFor_user:
                if (cartEntry.product.availableAmount < cartEntry.numOfProduct):
                    # as the item is not available after adding it to the card - supposedly another one bought it all
                    # return error
                    return False, "Some Items in cart are not available at the moment"

            # now checking is done so first we will generate a bill
            try:
                today = datetime.today().date()
                # fetching coupon details from coupon_id
                coupon, msg = couponDB.getCouponById(coupon_id=coupon_id)
                if coupon_id != None and coupon == None:
                    return None, "invalid coupon_id"
                bill = Bill(
                    user_id=user_id,
                    billAmount=cartSum,
                    coupon_id=coupon_id,
                    finalAmount=cartSum -
                    (cartSum*coupon.discount)/100 if coupon else cartSum,
                    date=today
                )
                db.session.add(bill)
                db.session.commit()

                # now creating order for record keeping
                # also updating card for bill id

                for entry in unboughtCartFor_user:
                    entry.product.availableAmount = entry.product.availableAmount - entry.numOfProduct

                    # creating the order
                    order = Order(bill_id=bill.id, product_id=entry.product_id,
                                  numOfProduct=entry.numOfProduct, totalSum=entry.totalSum)

                    db.session.add(order)
                    db.session.delete(entry)
                db.session.commit()
                return bill, f"Bill Generated. Id:{bill.id}"
            except IntegrityError as e:
                return None, "Error Occured"
            except SQLAlchemyError as e:
                return None, str(e.__dict__['orig'])

        else:
            return None, "No Items available in cart"
