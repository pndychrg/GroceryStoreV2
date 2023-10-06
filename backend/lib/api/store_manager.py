from datetime import timedelta
from flask_restful import Resource, request, reqparse
from flask_jwt_extended import create_access_token
from lib.methods.validators import Validators
from lib.db_utils.user_db import UserDB


# init userDB
userDB = UserDB()

# for post Method
create_storeManager_parser = reqparse.RequestParser()
create_storeManager_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
create_storeManager_parser.add_argument(
    "username", type=str, help="This field cannot be blank", required=True)
create_storeManager_parser.add_argument(
    "password", type=str, help="This field cannot be blank", required=True)


class StoreManagerAPI(Resource):

    def post(self):
        data = create_storeManager_parser.parse_args()
        if (Validators.name(data['name'])):
            return {"message": "Name can only contain alphabets"}

        if (Validators.username(data['username']) == False):
            return {'message': "username can only contain alphabets and numbers"}, 400

        # if all validators are successfull then set the manager as to be Registered

        response = userDB.registerUser(
            name=data['name'], username=data['username'], password=data["password"], role="notApproved")

        if response:
            # generating the token according to user
            token = create_access_token(
                identity=response.toJson(),
                expires_delta=timedelta(hours=8)
            )

            return {'token': token}, 200
        else:
            return {'message': "database error"}, 500
