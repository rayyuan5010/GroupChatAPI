from flask import Blueprint
from flask_restful import Api
from flask import current_app
from app.controllers.api import *
from flask_restful_swagger import swagger
from flask import current_app
from flask import Blueprint, Flask, redirect
API = Blueprint('api', __name__)
api = swagger.docs(
    Api(API),
    apiVersion="0.1",
    resourcePath="/",
    produces=["application/json"],
    api_spec_url="/spec",
    description="RestFul API",
)
api.add_resource(Version, '/version')

api.add_resource(SelfInfo, '/user/self/get')
api.add_resource(UserSignUp, '/user/insert')
api.add_resource(UserLogin, '/user/get')
api.add_resource(GetUsersSticker, '/user/sticker/get')
api.add_resource(UpdateFcmToken, '/user/token/update')
api.add_resource(AddNewGroup, '/group/insert')
api.add_resource(GetUserGroup, '/group/get')
api.add_resource(GetGroupAndFriendList, '/mixData/get')
api.add_resource(AddNewFriend, '/friend/insert')
api.add_resource(GetFriendInfo, '/friend/get')
api.add_resource(SendMessage2Friend, '/message/insert')


api.add_resource(UploadHeadshot, '/file/image/headshot/upload')
api.add_resource(GetHeadshot, '/file/image/headshot/')
api.add_resource(GetSticker, '/file/image/sticker/')
