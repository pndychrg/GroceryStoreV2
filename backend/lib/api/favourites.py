from flask_restful import Resource, request, reqparse
from lib.db_utils.favourites import FavouritesMethods
from flask_jwt_extended import jwt_required, get_jwt_identity
from lib.methods.decorators import checkJWTForUser


# init fav methods
favouritesMethods = FavouritesMethods()


class FavouritesAPI(Resource):

    @jwt_required()
    @checkJWTForUser
    def post(self, product_id=None):
        if product_id:
            # getting the user_id from access token
            user = get_jwt_identity()
            # backend method
            response, msg = favouritesMethods.addToFavourites(
                user_id=user.get('id'),
                product_id=product_id
            )
            if response:
                return response, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': "product_id not found"}, 400

    @jwt_required()
    @checkJWTForUser
    def get(self, product_id=None):
        # getting the user_id from access token
        user = get_jwt_identity()
        if product_id:
            response, msg = favouritesMethods.getFavouriteProduct(
                user_id=user.get('id'), product_id=product_id)
            if response:
                return response.product.toJson(), 200
            else:
                return {'msg': msg}, 400
        else:
            response, msg = favouritesMethods.getFavouritesForUser(
                user_id=user.get('id'))
            return [favProduct.product.toJson() for favProduct in response], 200
