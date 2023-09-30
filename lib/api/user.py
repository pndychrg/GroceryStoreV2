from datetime import timedelta
from flask_restful import Resource,request,reqparse,abort
from flask_jwt_extended import create_access_token,jwt_required
from lib.methods.validators import Validators
from lib.db_utils.user_db import UserDB
from flask import make_response,jsonify


# initializing User DB methods
userDB = UserDB()


# for POST method
create_user_parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate cannot be converted')
create_user_parser.add_argument("name",type=str,help="This field cannot be blank",required=True)
create_user_parser.add_argument("name",type=str,help="This field cannot be blank",required=True)
create_user_parser.add_argument("username",type=str,help="This field cannot be blank",required=True)
create_user_parser.add_argument("password",type=str,help="This field cannot be blank",required=True)

class UserAPI(Resource):

    def post(self):
        data = create_user_parser.parse_args()
        if(Validators.name(data['name'])):
            return make_response(jsonify({'message':"Name can only contain alphabets"}),404)
        if(Validators.username(data['username'])):
            return make_response(jsonify({'message':"username can only contain alphabets and numbers"}),404)
        # if all validations are successfull then add in database
        response = userDB.registerUser(name=data['name'],username=data['username'],password=data['password'])
        if response:
            # generating the token according to user 
            token = create_access_token(identity=response.toJson(),expires_delta=timedelta(hours=8))
            return {"token":token},200
        else:
            return make_response(jsonify({'message':"username already in use"}),404)
            