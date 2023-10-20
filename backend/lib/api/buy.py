from flask_restful import Resource, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.shop import ShopDB
from lib.methods.decorators import checkJWTForUser

# init
shopDB = ShopDB()


class BuyAPI(Resource):

    @jwt_required()
    @checkJWTForUser
    def post(self):

        # getting the user_id from jwt token
        user_id = get_jwt_identity().get('id')

        response, msg = shopDB.buy(
            user_id=user_id
        )
        if response:
            return response.toJson(), 200
        else:
            return {'msg': msg}, 400
