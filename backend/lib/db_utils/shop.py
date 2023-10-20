from models.bill import Bill
from models.products import Product
from models.order import Order
from lib.methods.validators import Validators
from lib.db_utils.cart import CartDB
from datetime import datetime
from extensions import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# init
validators = Validators()
cartDB = CartDB()


class ShopDB:

    def getBillsForUser(self, user_id):
        bills = Bill.query.filter_by(user_id=user_id).all()
        return bills

    def buy(self, user_id):

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
                bill = Bill(
                    user_id=user_id,
                    billAmount=cartSum,
                    # TODO WHEN ADDING COUPON CHANGE THIS FINAL AMOUNT VALUE
                    finalAmount=cartSum,
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
