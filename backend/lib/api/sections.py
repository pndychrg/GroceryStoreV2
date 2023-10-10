from flask_restful import Resource, request, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.sections import SectionDB
from lib.methods.validators import Validators
from lib.methods.decorators import *
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
        section, msg = sectionDB.getSectionById(section_id)
        if (section):
            return section.toJson(), 200
        else:
            return {'msg': msg}, 400

    @jwt_required()
    @checkJWTForAdmin
    def post(self):
        data = create_section_parser.parse_args()
        response, msg = sectionDB.addSection(
            name=data['name'].strip(), unit=data['unit'].strip()
        )
        if response:
            return response.toJson(), 200
        else:
            return {"msg": msg}, 400

    @jwt_required()
    @checkJWTForAdmin
    def put(self):
        # getting section id from params
        section_id = request.args.get("section_id")
        if (section_id == None):
            return {"msg": "section_id not found"}, 400
        data = update_section_parser.parse_args()
        if (Validators.name(data['name'])):
            return {"msg": "Name can only contain alphabets"}, 400
        if (Validators.checkStringForNull(data['unit'])):
            return {"msg": "Unit can't be null"}, 400

        response, msg = sectionDB.updateSection(
            section_id=section_id, name=data['name'].strip(), unit=data['unit'].strip())
        if response:
            return response.toJson(), 200
        else:
            return {"msg": msg}, 400

    @jwt_required()
    @checkJWTForAdmin
    def delete(self):
        # getting the section id from params
        section_id = request.args.get("section_id")
        if (section_id == None):
            return {"msg": "section_id not found"}, 400
        # validation
        if (Validators.checkForInt(section_id) == False):
            return {"msg": "section_id validation failed"}, 400
        # deleting the section
        response, msg = sectionDB.deleteSection(section_id=section_id)
        if (response):
            return response, 200
        else:
            return {'msg': msg}, 400


class GetAllSections(Resource):

    @jwt_required()
    @checkJWTForAdminOrManager
    def get(self):
        all_sections = sectionDB.getAllSections()
        # creating the json response
        response_json = [section.toJson() for section in all_sections]

        return response_json, 200


# for POST Method
create_section_request_parser = reqparse.RequestParser()
create_section_request_parser.add_argument(
    "name", type=str, help='This field cannot be blank', required=True
)
create_section_request_parser.add_argument(
    'unit', type=str, help='This field cannot be blank', required=True
)
create_section_request_parser.add_argument(
    "request", type=str, help='This field cannot be blank', required=True
)
create_section_request_parser.add_argument(
    "reg_section_id", type=str, help='This field cannot be blank', required=True
)


class SectionRequestsAPI(Resource):
    @jwt_required()
    @checkJWTForManager
    def post(self):
        data = create_section_request_parser.parse_args()
        response, msg = sectionDB.addSectionRequest(
            name=data['name'], unit=data['unit'], request=data['request'], reg_section_id=data['reg_section_id'])

        if response:
            return response.toJson(), 200
        else:
            return {'msg': msg}, 400

    @jwt_required()
    @checkJWTForAdminOrManager
    def get(self):
        # getting section_id from request args
        section_id = request.args.get("section_id")
        if section_id:
            response, msg = sectionDB.getSectionRequestById(section_id)
            if response:
                return response.toJson(), 200
            else:
                return {'msg': msg}, 400
        else:
            # send all section requests
            response, msg = sectionDB.getAllSectionRequests()
            if response:
                return [section.toJson() for section in response], 200
            else:
                return [], 200
    # TODO add sectionRequest put and delete methods here for managers to edit the sectionRequest before being updated
