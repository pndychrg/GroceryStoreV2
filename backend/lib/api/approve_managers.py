from flask_restful import Resource, request, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.user_db import UserDB
from lib.methods.decorators import checkJWTForAdmin

# init User DB
userDB = UserDB()


class ApproveManagerAPI(Resource):

    @jwt_required()
    @checkJWTForAdmin
    def get(self):
        unApprovedUser = userDB.getUnapproved()
        response = [user.toJson() for user in unApprovedUser]

        return response, 200
