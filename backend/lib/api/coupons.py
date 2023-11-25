from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from lib.db_utils.coupons import CouponDB
from lib.methods.decorators import checkJWTForManager, checkJWTForUser
from cache import cache
# init CouponMethods
couponDB = CouponDB()

# for coupon data parsing
coupon_parser = reqparse.RequestParser()
# defining the req parsers
coupon_parser = reqparse.RequestParser()
coupon_parser.add_argument(
    "coupon_code", help='This field cannot be blank', required=True)
coupon_parser.add_argument(
    "discount", help='This field cannot be blank', type=int, required=True)
coupon_parser.add_argument(
    "expiryDate", help='This field cannot be blank', required=True)


class CouponAPI(Resource):

    @jwt_required()
    @checkJWTForManager
    @cache.cached(timeout=30, query_string=True)
    def get(self, coupon_id=None):
        if coupon_id:
            coupon, msg = couponDB.getCouponById(coupon_id=coupon_id)
            return coupon.toJson(), 200
        else:
            coupons, msg = couponDB.getAllCoupons()
            return [coupon.toJson() for coupon in coupons], 200

    @jwt_required()
    @checkJWTForManager
    def post(self):
        data = coupon_parser.parse_args()
        response, msg = couponDB.createCoupon(
            coupon_code=data['coupon_code'],
            discount=data['discount'],
            expiryDate=data['expiryDate']
        )
        if response:
            return response.toJson(), 200
        else:
            return {'msg': msg}, 400

    @jwt_required()
    @checkJWTForManager
    def put(self, coupon_id=None):
        if coupon_id:
            data = coupon_parser.parse_args()
            response, msg = couponDB.editCoupon(
                coupon_id=coupon_id,
                coupon_code=data['coupon_code'],
                discount=data['discount'],
                expiryDate=data['expiryDate'],
            )
            print(f"{response} put method {msg}", flush=True)
            if response:
                return response.toJson(), 200
            else:
                return {"msg": msg}, 400
        else:
            return {'msg': "coupon_id not found"}, 400

    @jwt_required()
    @checkJWTForManager
    def delete(self, coupon_id=None):
        if coupon_id:
            response, msg = couponDB.deleteCoupon(coupon_id=coupon_id)
            if response:
                return response, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': "coupon_id not found"}, 400


class CouponsExtendedAPI(Resource):

    @jwt_required()
    @checkJWTForUser
    @cache.cached(timeout=30, query_string=True)
    def get(self, coupon_code=None):
        if coupon_code:
            coupon, msg = couponDB.getCouponByCode(coupon_code=coupon_code)
            if coupon:
                if coupon.hasExpired == 1:
                    return {'msg': "coupon has expired"}, 400
                return coupon.toJson(), 200
            else:
                return {'msg': "invalid coupon_code"}, 400
        else:
            coupons, msg = couponDB.getAllUnexpiredCoupons()
            return [coupon.toJson() for coupon in coupons], 200
