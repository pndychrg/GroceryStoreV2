from lib.db_utils.products import ProductDB
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from lib.methods.decorators import checkJWTForUserOrManager


# init productDB

productDB = ProductDB()


class SearchProductsAPI(Resource):

    @jwt_required()
    @checkJWTForUserOrManager
    def get(self):
        # getting data from request params
        name = request.args.get("name")
        rate = request.args.get('rate')
        section_id = request.args.get('section_id')
        manufactureDate = request.args.get('manufactureDate')
        print(section_id, flush=True)
        # fetching the products from the database
        products, msg = productDB.search_products(
            name=name,
            rate=rate,
            section_id=section_id,
            manufacture_date=manufactureDate
        )

        return [product.toJson() for product in products], 200
