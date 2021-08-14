#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: __init__.py
# Project: tools
# Created Date: Friday, April 2nd 2021, 10:44:16 am
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
import json
from flask import jsonify


def APIReturn(status: bool = True, data: any = None, message: str = None, errorCode: str = None):
    output = {'status': status}
    if data != None:
        if type(data) is dict or type(data) == type({}) or type(data) == list:
            output['data'] = data
        else:
            output['data'] = str(data)
        if type(data) == list:
            output['dataCount'] = len(data)
    if message != None and message != "":
        output['message'] = message
    if errorCode != None:
        output['code'] = errorCode

    return jsonify(output)
