#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: __init__.py
# Project: app
# Created Date: Thursday, April 1st 2021, 10:16:02 am
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

import traceback
import datetime
import json
import atexit
import random
import signal
import string
import sys
from threading import Thread
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import types
from sqlalchemy.orm.attributes import QueryableAttribute
from apscheduler.schedulers.background import BackgroundScheduler
from .config import SQLConfig

app = Flask(__name__, static_folder="../static")
app.config.from_object(SQLConfig)
db = SQLAlchemy(app)


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(
            self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:

                if type(getattr(self, key)) is datetime.datetime:
                    ret_data[key] = int(getattr(
                        self, key).timestamp())
                elif type(getattr(self, key)) is bytes:
                    ret_data[key] = getattr(self, key).decode()
                else:
                    ret_data[key] = getattr(self, key)
        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            print(f"check {check}")
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:

                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=('%s.%s' % (_path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data


def create_app():

    with app.app_context():
        app.config['SECRET_KEY'] = 'zxvz43y4y3sgz'
        app.config['app'] = app
        app.config['db'] = db
        app.config['BaseModel'] = BaseModel
        app.config["UPLOAD_FOLDER"] = "static"
        from . import models
        from .controllers import API
        db.init_app(app)

        app.register_blueprint(API, url_prefix="/api")
        db.create_all()
        db.session.commit()
        # NOTE: first time work
        # from .models import Region
        # a = Region.query.count()
        # try:
        #     if a == 0:
        #         from .job import getRegion
        #         getRegion()
        # except:
        #     pass

    return app
