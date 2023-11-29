from flask_restful import Resource, request, reqparse
from lib.db_utils.favourites import FavouritesMethods
from flask_jwt_extended import jwt_required, get_jwt_identity
from lib.methods.decorators import checkJWTForUser
from cache import cache


# init fav methods
favouritesMethods = FavouritesMethods()


# def make_key():
#     user = get_jwt_identity()
#     print(",".join([f"{key}={value}" for key, value in user.toJson().items()]))
#     return ",".join([f"{key}={value}" for key, value in user.toJson().items()])


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
                # Deleting the cache for the corresponding get endpoint
                # cache_key = f'favourite:get/{user.get("id")}/{product_id}'
                # cache.delete_memoized('get', cache_key)
                return response, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': "product_id not found"}, 400

    @jwt_required()
    @checkJWTForUser
    # @cache.cached(timeout=30)
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

    @jwt_required()
    @checkJWTForUser
    def delete(self, product_id=None):
        # getting the user from access token
        user = get_jwt_identity()
        if product_id:
            response, msg = favouritesMethods.removeFromFavourites(
                user_id=user.get('id'), product_id=product_id)

            if response:
                # deleting the cache of get method
                # cache.delete("")
                # Deleting the cache for the corresponding get endpoint
                # cache.delete(f"view//product/favourite")
                # cached_data = cache.get
                # cache.delete(f"flask_cache_/product/favourite")
                return response, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': 'product_id not found'}, 400
