#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: __init__.py
# Project: version
# Created Date: Thursday, April 1st 2021, 10:31:25 am
# Author: Ray
# -----
# Last Modified:
# Modified By:
# -----
# Copyright (c) 2021 Ray
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger


class Version(Resource):
    "Describing elephants"
    @swagger.operation(
        notes="get a todo item by ID",
        nickname="get",
        # Parameters can be automatically extracted from URLs.
        #   For Example: <string:id>
        # but you could also override them here, or add other parameters.
        parameters=[




            {
                "name": "sName",
                "description": "出租者名稱",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            },
            {
                "name": "sType",
                "description": "出租者身分",
                "required": True,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "path",
            },  {
                "name": "sPhone",
                "description": "連絡電話",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            }, {
                "name": "pType",
                "description": "型態",
                "required": True,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "path",
            }, {
                "name": "pStatus",
                "description": "現況",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            },
            {
                "name": "pSexReq",
                "description": "性別要求",
                "required": True,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "path",
            },
        ],
    )
    def post(self):

        # db = current_app.config['db']
        return '0.0.1'
