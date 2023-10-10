from flask_restful import Resource, request, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.user_db import UserDB
from lib.methods.decorators import checkJWTForAdmin

# init User DB
userDB = UserDB()

# approveManager
approveManager_parser = reqparse.RequestParser()
approveManager_parser.add_argument(
    "manager_id", type=int, help="This field cannot be blank", required=True)


class ApproveManagerAPI(Resource):

    @jwt_required()
    @checkJWTForAdmin
    def get(self):
        unApprovedUser = userDB.getUnapproved()
        if unApprovedUser:
            response = [user.toJson() for user in unApprovedUser]
        else:
            response = []
        return response, 200

    @jwt_required()
    @checkJWTForAdmin
    def post(self):
        data = approveManager_parser.parse_args()
        response, msg = userDB.approveManager(
            manager_id=data['manager_id'])
        if response:
            return {'msg': msg}, 200
        else:
            return {'msg': msg}, 400

    @jwt_required()
    @checkJWTForAdmin
    def delete(self):
        # getting the manager_id from request args
        manager_id = request.args.get("manager_id")
        if manager_id:
            response, msg = userDB.rejectManager(manager_id=manager_id)
            if response:
                return {'msg': msg}, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': "manager_id not found"}, 400
