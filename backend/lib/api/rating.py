from flask_restful import Resource, reqparse, request
from lib.db_utils.rating import RatingMethods
from flask_jwt_extended import jwt_required, get_jwt_identity
from lib.methods.decorators import checkJWTForUser
from cache import cache

# init fav methods
ratingMethods = RatingMethods()

# parser for post method
rate_product = reqparse.RequestParser()
rate_product.add_argument("product_id", required=True,
                          help="This Field cannot be blank", type=int)
rate_product.add_argument(
    "rating", help="This field cannot be blank", type=int)
rate_product.add_argument(
    "comment", type=str, required=True, help='This Field cannot be blank'
)


class RatingsAPI(Resource):

    @jwt_required()
    @checkJWTForUser
    def post(self):
        data = rate_product.parse_args()
        response, msg = ratingMethods.rateProduct(
            user_id=get_jwt_identity().get('id'),
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data['comment']
        )

        if response:
            return response.toJson(), 200

        else:
            return {'msg': msg}, 400

    @jwt_required()
    @checkJWTForUser
    @cache.cached(timeout=30, query_string=True)
    def get(self, product_id=None):
        response, msg = ratingMethods.getProductRatingForUser(
            user_id=get_jwt_identity().get('id'), product_id=product_id)
        if response:
            print(response, flush=True)
            return response.toJson(), 200
        else:
            return {"msg": msg}, 400

    @jwt_required()
    @checkJWTForUser
    def delete(self, product_id=None):
        response, msg = ratingMethods.deleteRating(
            user_id=get_jwt_identity().get('id'), product_id=product_id)
        if response:
            return response, 200
        else:
            return {'msg': msg}, 400
