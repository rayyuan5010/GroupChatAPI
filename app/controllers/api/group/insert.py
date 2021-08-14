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


class AddNewGroup(Resource):
    def post(self):
        try:
            from ....models import Group, GroupMember
            name = request.json.get('name')
            image = request.json.get('image')
            owner = request.json.get('owner')
            # if name == None
            group = Group(
                name=name,
                owner=owner,
                image=image
            )
            groupId = group.save()
            groupMember = GroupMember(
                userId=owner,
                groupId=groupId
            )
            groupMember.save()
            return APIReturn(status=True, data=dict(
                id=groupId
            ))
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=f"[{exc_tb.tb_lineno}]{str(e)}")
