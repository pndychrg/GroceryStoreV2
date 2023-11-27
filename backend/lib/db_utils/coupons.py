from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from extensions import db
from models.coupon import Coupon
from models.bill import Bill
from lib.methods.validators import Validators

validators = Validators()


class CouponDB:

    # get all coupons
    def getAllUnexpiredCoupons(self):
        coupons = Coupon.query.filter_by(hasExpired=0)
        return coupons, "Unexpired Coupons"

    # get all coupons
    def getAllCoupons(self):
        coupons = Coupon.query.all()
        return coupons, "All Coupons"

    # get All coupons by code
    def getCouponByCode(self, coupon_code):
        existingCoupon = Coupon.query.filter(
            Coupon.coupon_code.like(f"{coupon_code}")).first()
        if existingCoupon:
            return existingCoupon, "Coupon Found"
        else:
            return None, "Coupon not found"

    def getCouponById(self, coupon_id):
        return Coupon.query.get(coupon_id), "Coupon Details"

    def createCoupon(self, coupon_code, discount, expiryDate):
        # validating date
        if (Validators.checkDate(expiryDate) == False):
            return None, "invalid expiryDate"
        else:
            expiryDate = datetime.strptime(
                expiryDate, '%Y-%m-%d'
            ).date() if (expiryDate != None) and (len(expiryDate) != 0) else None
        # validating couponcode and discount
        if Validators.checkStringForNull(coupon_code):
            return None, "invalid coupon_code"
        # TODO try without validation for integer
        if Validators.checkForInt(discount) == False:
            return None, "invalid discount"

        # checking if discount is less than 100
        if discount > 100:
            return None, "invalid discount"
        # try catch
        try:
            new_coupon = Coupon(
                coupon_code=coupon_code,
                discount=discount,
                expiryDate=expiryDate,
                hasExpired=0
            )
            db.session.add(new_coupon)
            db.session.commit()
            return new_coupon, "Coupon created"

        except IntegrityError as e:
            return None, "Coupon with same code already exists"
        except SQLAlchemyError as e:
            return None, str(e.__dict__['orig'])

    def editCoupon(self, coupon_id, coupon_code, discount, expiryDate=None):
        # validating date
        if (Validators.checkDate(expiryDate) == False):
            return None, "invalid expiryDate"
        else:
            expiryDate = datetime.strptime(
                expiryDate, '%Y-%m-%d'
            ).date() if (expiryDate != None) and (len(expiryDate) != 0) else None
        # validating couponcode and discount
        if Validators.checkStringForNull(coupon_code):
            return None, "invalid coupon_code"
        # TODO try without validation for integer
        if Validators.checkForInt(discount) == False:
            return None, "invalid discount"

        # finding the existing coupon through id
        existingCoupon, msg = self.getCouponById(coupon_id=coupon_id)
        print(existingCoupon.toJson(), flush=True)
        print("Yes")
        if coupon_id:
            try:
                existingCoupon.coupon_code = coupon_code
                existingCoupon.discount = discount
                existingCoupon.expiryDate = expiryDate
                existingCoupon.hasExpired = 0
                db.session.commit()
                return existingCoupon, "Coupon Edited successfully"
            except IntegrityError as e:
                return None, "Coupon Code already exists"
            except SQLAlchemyError as e:
                return None, str(e.__dict__['orig'])
        else:
            return None, "invalid coupon_id"

    def deleteCoupon(self, coupon_id):
        coupon, msg = self.getCouponById(coupon_id=coupon_id)
        if coupon:
            # check if coupon is being used anywhere
            bills = Bill.query.filter(Bill.coupon_id == coupon.id).first()
            if bills:
                return False, "Coupon is used in a bill"
            db.session.delete(coupon)
            db.session.commit()
            return True, "Coupon Deleted"
        else:
            return False, "invalid coupon_id"

    def updateExpirationValue(self):
        coupons, msg = self.getAllCoupons()
        today = datetime.today()
        for coupon in coupons:
            # all the unexpired coupons are fetched
            if coupon.expiryDate:
                if coupon.expiryDate < today:
                    coupon.hasExpired = 1
        db.session.commit()
