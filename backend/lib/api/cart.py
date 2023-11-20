from flask_restful import Resource, request, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.cart import CartDB
from lib.methods.decorators import checkJWTForUser
# init
cartDB = CartDB()


# add to cart req parser
cart_parser = reqparse.RequestParser()
cart_parser.add_argument(
    "product_id", type=int, help='This Field cannot be blank', required=True)
cart_parser.add_argument(
    "numOfProduct", type=int, help='This Field cannot be blank', required=True)


class CartAPI(Resource):

    @jwt_required()
    @checkJWTForUser
    def get(self):
        # getting the user_id from token
        userFromToken = get_jwt_identity()

        # getting the cart for user_id
        cartItems, cartSum = cartDB.getCartProducts(
            user_id=userFromToken.get('id'))

        return {
            "cart": [cart.toJson() for cart in cartItems],
            "sum": cartSum
        }, 200

    @jwt_required()
    @checkJWTForUser
    def post(self):
        # getting the user_id from the jwt token
        userFromToken = get_jwt_identity()
        # print(userFromToken, flush=True)
        # user_id = 3
        # parsing
        data = cart_parser.parse_args()
        response, msg = cartDB.addToCart(
            user_id=userFromToken.get('id'),
            product_id=data['product_id'],
            numOfProduct=data['numOfProduct']
        )
        if response:
            return response.toJson(), 200
        else:
            return {'msg': "Error Occured"}, 500

    @jwt_required()
    @checkJWTForUser
    def delete(self):
        # getting the user_id from the jwt token
        userFromToken = get_jwt_identity()
        product_id = request.args.get('product_id')
        if product_id:
            response, msg = cartDB.removeFromCart(
                product_id=product_id, user_id=userFromToken.get('id'))
            if response:
                return response, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': 'cart_id not found'}, 400
