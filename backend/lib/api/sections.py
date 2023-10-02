from flask_restful import Resource, request, reqparse
from flask_jwt_extended import jwt_required
from lib.db_utils.sections import SectionDB

# init Section DB
sectionDB = SectionDB()

# for POST Method
create_section_parser = reqparse.RequestParser()
create_section_parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True)
