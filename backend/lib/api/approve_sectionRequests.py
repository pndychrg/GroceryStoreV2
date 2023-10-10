from flask_restful import Resource, reqparse, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.db_utils.sections import SectionDB
from lib.methods.decorators import checkJWTForAdmin

sectionDB = SectionDB()


class ApproveSectionRequests(Resource):

    @jwt_required()
    @checkJWTForAdmin
    def get(self):
        # getting the sectionRequest id from section request
        section_id = request.args.get("section_id")
        # if section id is found
        if section_id:
            # fetch the sectionRequest from database
            sectionRequest, message = sectionDB.getSectionRequestById(
                section_id=section_id)
            # print(sectionRequest.toJson(), flush=True)
            # check what is the request
            # if the section request is add then add the sectionRequest to section database
            if sectionRequest.request == 'add':
                # creating the section
                response, message = sectionDB.addSection(
                    name=sectionRequest.name, unit=sectionRequest.unit)
                if response:
                    # now as the section request is approved, so delete it from the section Requests table
                    sectionDB.deleteSectionRequestById(sectionRequest.id)
                    return response.toJson(), 200
                else:
                    return {'msg': message}, 400
            elif sectionRequest.request == 'edit' and sectionRequest.reg_section_id != None:
                # then fetch the registered section from database using the reg_section_id
                # reg_section = sectionDB.getSectionById(section_id=sectionRequest.reg_section_id)
                # if section is found
                # now update the section values
                response, message = sectionDB.updateSection(
                    section_id=sectionRequest.reg_section_id, name=sectionRequest.name, unit=sectionRequest.unit)
                if response:
                    # as it is approved then clear it from the sectionRequest table
                    sectionDB.deleteSectionRequestById(sectionRequest.id)
                    return response.toJson(), 200
                else:
                    return {'msg': message}, 400
            # there can only be three options for change requests 'add','edit','delete'
            else:
                response, message = sectionDB.deleteSection(
                    section_id=sectionRequest.reg_section_id)
                if response:
                    # as it is approved then clear it from the sectionRequest table
                    sectionDB.deleteSectionRequestById(sectionRequest.id)
                    # here response will be True
                    return response, 200
                else:
                    return {'msg': message}, 400

        else:
            # return error
            return {'msg': "section_id not found"}, 400

    # this method is for handling rejection by the admin
    @jwt_required()
    @checkJWTForAdmin
    def delete(self):
        # getting the sectionRequest id from the request args
        section_id = request.args.get("section_id")
        if section_id:
            response, msg = sectionDB.deleteSectionRequestById(
                section_id=section_id)
            if response:
                return True, 200
            else:
                return {'msg': msg}, 400
        else:
            return {'msg': "section_id not found"}, 400
