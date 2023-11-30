from datetime import timedelta
from flask_restful import Resource, request, reqparse, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from lib.methods.decorators import checkJWTForUser
from lib.methods.validators import Validators
from lib.db_utils.user_db import UserDB
from werkzeug.datastructures import FileStorage
from cache import cache
from lib.jobs.forgot_password import send_updated_password_mail
# initializing User DB methods
userDB = UserDB()

# for POST method
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
create_user_parser.add_argument(
    "username", type=str, help="This field cannot be blank", required=True)
create_user_parser.add_argument(
    "email", type=str, help="This field cannot be blank",
    required=True
)
create_user_parser.add_argument(
    "password", type=str, help="This field cannot be blank", required=True)
create_user_parser.add_argument(
    "role", type=str
)

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument(
    "name", type=str, required=True, help="This Field cannot be blank",
)
update_user_parser.add_argument(
    "username", type=str, required=True, help="This Field cannot be blank"
)
update_user_parser.add_argument(
    "email", type=str, help="This Field cannot be blank",
    required=True
)
update_user_parser.add_argument(
    "id", type=str, help="This Field cannot be blank",
    required=True
)
update_user_parser.add_argument(
    "password", type=str, required=True, help="This Field cannot be blank"
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
            name=data['name'], username=data['username'], email=data['email'], password=data['password'], role=data['role'] if data['role'] else "user")
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

    @jwt_required()
    def put(self):
        data = update_user_parser.parse_args()
        response, msg = userDB.updateUser(
            user_id=data['id'],
            name=data['name'],
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        if response:
            # generating the updated token because all user data is managed through it
            token = create_access_token(
                identity=response.toJson(), expires_delta=timedelta(hours=8)
            )
            return {'token': token}, 200
        else:
            return {'msg': msg}, 400


class UserRatingAPI(Resource):

    @jwt_required()
    @checkJWTForUser
    @cache.cached(timeout=30, query_string=True)
    def get(self):
        # getting user_id from jwt
        user_id = get_jwt_identity().get('id')
        # fetching the user from user_id to get the complete user details
        user = userDB.getUser(user_id=user_id)
        # now sending the rating
        # print(user.toJson(), flush=True)
        return [rating.toJson() for rating in user.ratings], 200


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# request Parser for user image
user_img = reqparse.RequestParser()
user_img.add_argument(
    'image', type=FileStorage, location='files'
)


class UserImageAPI(Resource):

    @jwt_required()
    def post(self):
        # fetching the user_id from jwttoken
        user_id = get_jwt_identity().get('id')
        data = user_img.parse_args()
        # uploaded image
        uploaded_img = data.get('image')
        if uploaded_img:
            if allowed_image(uploaded_img.filename):
                # reading the data as bytes
                img_data = uploaded_img.read()
                if img_data:
                    response, msg = userDB.setUserImage(
                        user_id=user_id, image=img_data)
                    if response:
                        return response.image(), 200
                    else:
                        return {'msg': msg}, 400
                else:
                    return {'msg': 'Image Data is empty'}, 400
            else:
                return {'msg': "Invalid image format"}, 400
        else:
            response, msg = userDB.setUserImage(
                user_id=user_id,
                image=None
            )
            if response:
                return response.toJson(), 200
            else:
                return {'msg': msg}, 400

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity().get('id')
        # fetching user from database
        user = userDB.getUser(user_id=user_id)
        # returning only the user img
        return user.image(), 200


userPasswordUpdateParser = reqparse.RequestParser()
userPasswordUpdateParser.add_argument(
    "new_password", required=True, type=str, help="this field is required")
userPasswordUpdateParser.add_argument(
    "current_password", required=True, type=str, help="This field is required"
)


class UserPasswordUpdate(Resource):

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity().get('id')
        data = userPasswordUpdateParser.parse_args()

        response, msg = userDB.updateUserPassword(
            user_id=user_id, current_password=data['current_password'], new_password=data['new_password'])
        if response:
            return {'msg': msg}, 200
        else:
            # print(response, msg, flush=True)
            return {'msg': msg}, 400

    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        user_id = user.get('id')
        updated_password = userDB.setRandomPassword(user_id=user_id)
        data = {
            "user": get_jwt_identity(),
            "password": updated_password

        }
        job = send_updated_password_mail.apply_async(args=[data])
        result = job.wait()
        return {'msg': "Password Updated"}, 200
