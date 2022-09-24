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
            tmessage = request.form.get('message')
            debug = request.form.get('debug')
            # print(message)

            old_message = json.loads(tmessage)
            senderId = request.form.get('senderId')
            if senderId == None or senderId == None:
                return APIReturn(status=False, message="need sender or receiver", errorCode="0x0000000101")
            userData = User.query.filter(User.id == senderId).one()
            '''
            "senderId": Authentication.user.id,
            "senderName": "name",
            "senderImage": "image",
            "reciver": "",
            "reciveType": "0",
            "messageId": "${Authentication.user.id}-${time}",
            "messageType": "0",
            "messageTime": "$time",
            "messageContent": message,
            "messageTabId": "0"
            '''
            message = Message(
                messageId=old_message['messageId'],
                messageContent=old_message['messageContent'],
                receiverId=old_message['reciver'],
                senderId=old_message['senderId'],

            )
            message.save()

            userData2 = User.query.filter_by(
                id=receiverId).one()
            # print("receiverId", receiverId)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=AAAA8txAe6s:APA91bH9NwAC6OCWGlsCWylqKPwkOY4_S-fn6vMBIoUYZuhptk70BqnpGWAyS9EJ1mzqG5dzQteFUqgfDjbbaxYzEIZjR-17gLHBXVnWUrs4qPD7aqyaWJ4RX6lJx2TbPkU6f30s3zME',
                'Content-Type': 'application/json'
            }
            url = 'https://fcm.googleapis.com/fcm/send'
            # print(message)
            payload = {
                "registration_ids": [userData2.fcmToken],
                "notification": {
                    "title": userData.name,
                    "body": message.messageContent
                },
                "collapse_key": "type_a",
                "data": old_message
            }
            print(json.dumps(payload))
            resp = requests.post(url, headers=headers,
                                 data=json.dumps(payload))

            print(resp.text.encode('utf8'), flush=True)

            return APIReturn(status=True, data=message.to_dict())
        except SQLAlchemyError as se:
            print(se)
            return APIReturn(status=False, errorCode="0x0000000102", message=str(se))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000103", message=str(e))
