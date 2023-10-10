from datetime import timedelta
from flask_restful import Resource, request, reqparse, abort
from flask_jwt_extended import create_access_token, jwt_required
from lib.methods.validators import Validators
from lib.db_utils.user_db import UserDB


# initializing User DB methods
userDB = UserDB()

# for POST method
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
create_user_parser.add_argument(
    "username", type=str, help="This field cannot be blank", required=True)
create_user_parser.add_argument(
    "password", type=str, help="This field cannot be blank", required=True)
create_user_parser.add_argument(
    "role", type=str
)


class UserAPI(Resource):

    def post(self):
        data = create_user_parser.parse_args()
        if (Validators.name(data['name'])):
            return {'msg': "Name can only contain alphabets"}, 400
        if (Validators.username(data['username']) == False):
            return {'msg': "username can only contain alphabets and numbers"}, 400
        # if all validations are successfull then add in database
        response, msg = userDB.registerUser(
            name=data['name'], username=data['username'], password=data['password'], role=data['role'] if data['role'] else "user")
        if response:
            # generating the token according to user
            token = create_access_token(
                identity=response.toJson(), expires_delta=timedelta(hours=8))
            return {"token": token}, 200
        else:
            return {'msg': msg}, 400

    def get(self):
        username = request.args.get("username")
        password = request.args.get("password")

        # check if username and password are present or not
        if (username == None):
            return {'msg': "username not found in request"}, 400
        if (password == None):
            return {'msg': "password not found in request"}, 400
        if (Validators.username(username=username) == False):
            return {'msg': "username can only contain alphabets and numbers"}, 400

        # if all validations are successfull then add in database
        response = userDB.loginUser(username=username, password=password)
        # resonse[0] = msg from db(user if true) , response[1] = boolean T/F
        if response[1]:
            # generating the token
            token = create_access_token(
                identity=response[0].toJson(), expires_delta=timedelta(hours=8))
            return {'token': token}, 200
        else:
            return {'msg': response[0]}, 400
