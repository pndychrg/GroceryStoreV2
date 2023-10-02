from flask_restful import Resource, request, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.sections import SectionDB

# init Section DB
sectionDB = SectionDB()

# for POST Method
create_section_parser = reqparse.RequestParser()
create_section_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
create_section_parser.add_argument(
    "unit", type=str, help="This field cannot be blank", required=True)


class SectionAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        # getting the section id from the request parameters
        section_id = request.args.get("section_id")
        if current_user.get("role") != "user":
            section, message = sectionDB.getSectionById(section_id)
            if (section):
                return section.toJson(), 200
            else:
                return {'message': message}, 404
