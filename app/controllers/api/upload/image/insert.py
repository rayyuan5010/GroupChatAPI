from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from .....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
import shortuuid
import os


class UploadHeadshot(Resource):
    def post(self):
        try:
            from .....models import User
            # uid = request.json.get('id')
            userId = request.form.get('id')
            print(userId)
            image = request.files.get('file')
            filename = f"f_{userId}_{shortuuid.ShortUUID().random(length=10)}"
            print(os.path.exists(
                f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}'))
            print(f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}')
            if not os.path.exists(f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}'):
                print("123123")
                os.mkdir(f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}')
                os.mkdir(
                    f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}/images/')
                os.mkdir(
                    f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}/files/')
            image.save(
                f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}/images/{filename}')
            print(
                f'app/{current_app.config["UPLOAD_FOLDER"]}/{userId}/images/{filename}')
            userData: User = User.query.filter_by(
                id=userId).one()
            userData.image = filename
            userData.update()
            return APIReturn(data={"filename": filename})
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=str(e))
