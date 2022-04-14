from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from ....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
import shortuuid


class UserSignUp(Resource):
    def post(self):
        try:
            from ....models import User
            # uid = request.json.get('id')
            debug = request.form.get('debug')
            print(debug)
            if debug == None or debug == False:
                email = request.form.get('email')
                password = request.form.get('password')
                if email == None or password == None:
                    return APIReturn(status=False, message="need email and password", errorCode="0x0000000101")
                user = User(
                    id=shortuuid.ShortUUID().random(length=20),
                    email=email,
                    password=password,
                    friendCode=shortuuid.ShortUUID().random(length=20)
                )
                user.save()
            else:
                from randomuser import RandomUser

                # Generate a single user
                tempuser = RandomUser()
                user = User(
                    id=shortuuid.ShortUUID().random(length=20),
                    email=tempuser.get_email(),
                    password=tempuser.get_password(),
                    name=tempuser.get_full_name(),
                    friendCode=shortuuid.ShortUUID().random(length=20)
                )
                user.save()
            return APIReturn(status=True, data=user.to_dict())
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=str(e))


class UpdateFcmToken(Resource):
    def post(self):
        try:
            from ....models import User
            # uid = request.json.get('id')
            uid = request.form.get('AuthID')

            token = request.form.get('token')
            print(uid)
            if uid == None or token == None:
                return APIReturn(status=False, message="need uid or token", errorCode="0x0000000101")
            user: User = User.query.filter_by(
                id=uid).one()
            user.fcmToken = token
            user.update()

            return APIReturn(status=True, data=user.to_dict())
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=str(e))
