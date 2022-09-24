from flask_restful import Resource
from flask import current_app, send_file
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from .....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
import shortuuid
import os


class GetHeadshot(Resource):
    def get(self):
        try:
            from .....models import User
            # uid = request.json.get('id')
            # userId = request.form.get('id')
            args = request.args
            userId = args['i']

            user: User = User.query.filter_by(
                id=userId).one()
            print(
                f'{current_app.config["UPLOAD_FOLDER"]}/{userId}/images/{user.image}')
            return send_file(f'{current_app.config["UPLOAD_FOLDER"]}/{userId}/images/{user.image}')
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=str(e))
