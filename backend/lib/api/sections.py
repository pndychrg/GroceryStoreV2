from flask_restful import Resource, request, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.sections import SectionDB
from lib.methods.validators import Validators
from lib.methods.decorators import checkJWTForAdmin
# init Section DB
sectionDB = SectionDB()

# for POST Method
create_section_parser = reqparse.RequestParser()
create_section_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
create_section_parser.add_argument(
    "unit", type=str, help="This field cannot be blank", required=True)

# for PUT Method
update_section_parser = reqparse.RequestParser()
update_section_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
update_section_parser.add_argument(
    "unit", type=str, help="This field cannot be blank", required=True)


class SectionAPI(Resource):

    @jwt_required()
    @checkJWTForAdmin
    def get(self):
        # getting the section id from the request parameters
        section_id = request.args.get("section_id")
        section, message = sectionDB.getSectionById(section_id)
        if (section):
            return section.toJson(), 200
        else:
            return {'message': message}, 400

    @jwt_required()
    @checkJWTForAdmin
    def post(self):
        current_user = get_jwt_identity()
        data = create_section_parser.parse_args()
        if (Validators.name(data['name'])):
            return {"message": "Name can only contain alphabets"}, 404
        if (Validators.checkStringForNull(data['unit'])):
            return {"message": "Unit can't be null"}, 400
        response, message = sectionDB.addSection(
            name=data['name'].strip(), unit=data['unit'].strip()
        )
        if response:
            return response.toJson(), 200
        else:
            return {"message": message}, 400

    @jwt_required()
    @checkJWTForAdmin
    def put(self):
        # getting section id from params
        section_id = request.args.get("section_id")
        if (section_id == None):
            return {"message": "section_id not found"}, 400
        data = update_section_parser.parse_args()
        if (Validators.name(data['name'])):
            return {"message": "Name can only contain alphabets"}, 400
        if (Validators.checkStringForNull(data['unit'])):
            return {"message": "Unit can't be null"}, 400

        response, message = sectionDB.updateSection(
            section_id=section_id, name=data['name'].strip(), unit=data['unit'].strip())
        if response:
            return response.toJson(), 200
        else:
            return {"message": message}, 400

    @jwt_required()
    @checkJWTForAdmin
    def delete(self):
        # getting the section id from params
        section_id = request.args.get("section_id")
        if (section_id == None):
            return {"message": "section_id not found"}, 400
        # validation
        if (Validators.checkForInt(section_id) == False):
            return {"message": "section_id validation failed"}, 400
        # deleting the section
        response, message = sectionDB.deleteSection(section_id=section_id)
        if (response):
            return response, 200
        else:
            return {'message': message}, 400
