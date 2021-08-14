from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from ....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
import sys
import os


class GetUserGroup(Resource):
    def post(self):
        try:
            from ....models import Group, GroupMember
            userId = request.form.get('userId')
            if userId == None:
                return APIReturn(status=False, message="need user ID")
            groups = Group.query.join(
                GroupMember, GroupMember.groupId == Group.id) .filter(GroupMember.userId == userId).all()
            output = []
            for o in groups:
                output.append(o.to_dict())
            return APIReturn(status=True, data=output, message=userId)
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=f"[{exc_tb.tb_lineno}]{str(e)}")
