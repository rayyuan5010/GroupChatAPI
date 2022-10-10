from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from .....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError


class GetUsersSticker(Resource):
    def post(self):
        try:
            from .....models import User, UsersSticker
            id = request.form.get('userId')

            userData = User.query.filter_by(
                id=id).one()
            if not userData is None:
                # return APIReturn(status=True, data=userData.to_dict())
                usersSticker: UsersSticker = UsersSticker.query.filter_by(
                    user=id).all()
                datas = []
                for o in usersSticker:
                    datas.append(o.to_dict())
                return APIReturn(status=True, data=datas)
            else:
                return APIReturn(status=False, errorCode="0x0000000204", message="找不到帳號或密碼錯誤")

        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000202", message=str(se.__dict__))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000203", message=e.toString())
