from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from ....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError


class UserLogin(Resource):
    "登入"
    @swagger.operation(
        notes="使用者登入",
        nickname="UserLogin",
        parameters=[
            {
                "name": "email",
                "description": "信箱",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "query",
            }, {
                "name": "password",
                "description": "密碼",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "query",
            },
        ]
    )
    def post(self):
        try:
            from ....models import User
            email = request.form.get('email')
            password = request.form.get('password')
            if email == None or password == None:
                return APIReturn(status=False, message="need email and password", errorCode="0x0000000201")
            userData = User.query.filter_by(
                email=email).filter_by(password=password).one()
            if not userData is None:
                return APIReturn(status=True, data=userData.to_dict())
            else:
                return APIReturn(status=False, errorCode="0x0000000204", message="找不到帳號或密碼錯誤")

        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000202", message=str(se.__dict__['orig']))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000203", message=e.toString())
