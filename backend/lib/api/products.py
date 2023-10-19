from lib.db_utils.products import ProductDB
from extensions import db
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from lib.methods.decorators import checkJWTForManager, checkJWTForUserOrManager

# for POST Method
create_product_parser = reqparse.RequestParser()
create_product_parser.add_argument(
    "name", type=str, help='This field cannot be blank', required=True
)
create_product_parser.add_argument(
    "availableAmount", type=int, help='This field cannot be blank', required=True
)
create_product_parser.add_argument(
    'rate', type=int, help='This field cannot be blank', required=True
)
create_product_parser.add_argument(
    'section_id', type=int, help='This field section cannot be blank', required=True
)
create_product_parser.add_argument(
    "manufactureDate", type=str, help='This field cannot be blank', required=True
)
create_product_parser.add_argument(
    "expiryDate", type=str, help='This field cannot be blank', required=True
)


# init productDB
productDB = ProductDB()


class ProductsAPI(Resource):

    @jwt_required()
    @checkJWTForUserOrManager
    def get(self):
        # TODO add getProductBysectionID
        # TODO add getProductByProductID
        products = productDB.getAllProducts()
        # print(products, flush=True)
        # if products:
        return [product.toJson() for product in products], 200
        # else:
        #     [], 200

    @jwt_required()
    @checkJWTForManager
    def post(self):
        data = create_product_parser.parse_args()
        # TODO create better method for section_id validaiton
        if data['section_id']:
            response, msg = productDB.addProduct(
                name=data['name'].strip(),
                availableAmount=data['availableAmount'],
                rate=data['rate'],
                manufactureDate=data['manufactureDate'],
                expiryDate=data['expiryDate'],
                section_id=data['section_id']
            )

            if response:
                return response.toJson(), 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': "section_id not found"}, 400

    @jwt_required()
    @checkJWTForManager
    def put(self):
        # getting the product id from params
        product_id = request.args.get('product_id')
        if (product_id == None):
            return {"msg": "product_id not found"}, 400

        # parsing the data
        data = create_product_parser.parse_args()
        response, msg = productDB.updateProduct(
            product_id=product_id,
            name=data['name'],
            availableAmount=data['availableAmount'],
            rate=data['rate'],
            manufactureDate=data['manufactureDate'],
            expiryDate=data['expiryDate'],
            section_id=data['section_id']
        )
        if response:
            return response.toJson(), 200
        else:
            return {'msg': msg}, 400

    @jwt_required()
    @checkJWTForManager
    def delete(self):
        product_id = request.args.get('product_id')

        if product_id:
            response, msg = productDB.deleteProductById(product_id=product_id)
            if response:
                return True, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': 'product_id not found'}, 400
