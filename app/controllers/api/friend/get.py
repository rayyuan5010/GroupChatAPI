from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import and_, or_
from ....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
import sys
import os


class GetFriendInfo(Resource):
    def post(self):
        try:
            from ....models import FriendList, User
            userId = request.form.get('userId')
            friendId = request.form.get('friendId')
            friendData = None
            friend: FriendList = FriendList.query.filter(

                and_(FriendList.userId == userId,
                     FriendList.friendId == friendId),



            ).one()
            if friend is not None:
                user: User = User.query.filter_by(id=friendId).one()
                friendData = user.to_dict()

                del friendData['password']

            if friendData is None:
                return APIReturn(status=False, errorCode="0x0000000104", message="not a friend")
            else:
                return APIReturn(data=friendData)
        except SQLAlchemyError as se:
            print(se.__dict__)
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=f"[{exc_tb.tb_lineno}]{str(e)}")
