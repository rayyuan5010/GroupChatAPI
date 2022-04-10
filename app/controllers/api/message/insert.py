from typing import List
from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from ....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
import shortuuid
import datetime
import requests


class SendMessage2Friend(Resource):
    def post(self):
        try:
            from ....models import User, Message

            receiverId = request.form.get('receiverId')
            message = request.form.get('message')
            debug = request.form.get('debug')
            if debug == None or debug == False:
                senderId = request.form.get('senderId')
                if senderId == None or senderId == None:
                    return APIReturn(status=False, message="need sender or receiver", errorCode="0x0000000101")
                message = Message(
                    id=f"{senderId}-{datetime.datetime.now()}",
                    messageContent=message,
                    receiverId=receiverId,
                    senderId=senderId
                )
                message.save()
            else:
                userDatas: List = User.query.all()
                userData: User = userDatas[0]
                message = Message(
                    id=f"{userData.id}-{datetime.datetime.now()}",
                    messageContent=message,
                    receiverId=receiverId,
                    senderId=userData.id
                )
                message.save()
            userData2 = User.query.filter_by(
                id=receiverId).one()

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=AAAAxF-fPxs:APA91bEONS_MTChz6nFZuEwcvzir_kpTM4RHnTCL1S-O9aL3hXClZ1kBLbzxQpVHq_upAgUHqCYeRoqhmsU40EyQ5qhN-KH-M20ZpguDPAdJXCeZLaz28Y-2VQTWfe3yCPSHps91L2YmOTUpfHjYmaFGP6FQXsKsbA',
                'Content-Type': 'application/json'
            }
            url = 'https://fcm.googleapis.com/fcm/send'
            print(message)
            payload = {
                "registration_ids": [userData2.fcmToken],
                "notification": {
                    "title": userData.name,
                    "body": message.messageContent
                },
                "collapse_key": "type_a",
                "data": message.to_dict()
            }
            print(json.dumps(payload))
            resp = requests.post(url, headers=headers,
                                 data=json.dumps(payload))

            print(resp.text.encode('utf8'), flush=True)

            return APIReturn(status=True, data=message.to_dict())
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se.__dict__['orig']))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=str(e))
