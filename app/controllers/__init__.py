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


api.add_resource(UserSignUp, '/user/insert')
api.add_resource(UserLogin, '/user/get')
api.add_resource(AddNewGroup, '/group/insert')
api.add_resource(GetUserGroup, '/group/get')
