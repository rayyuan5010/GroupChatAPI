from app.controllers.api import group
from flask_restful import Resource
from flask import current_app
from flask_restful_swagger import swagger
from flask import request
from sqlalchemy import or_
from ....tools import *
from app.tools import APIReturn
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_


class GetGroupAndFriendList(Resource):

    def post(self):
        try:
            from ....models import Group, GroupMember, FriendList, User
            db = current_app.config['db']
            userId = request.form.get('userId')
            if userId == None:
                return APIReturn(status=False, message="need user ID")
            groups = Group.query.join(
                GroupMember, GroupMember.groupId == Group.id) .filter(GroupMember.userId == userId).all()
            lGroupList = []
            for o in groups:
                lGroupList.append(o.to_dict())
            lFriendList = []
            friends = db.session.query(FriendList, User).join(
                User, FriendList.friendId == User.id).filter(FriendList.userId == userId).all()
            for f, u in friends:
                u: User
                lFriendList.append(dict(
                    name=u.name,
                    id=u.id,
                    image=u.image,
                    userSM=u.userSM
                ))
            data = dict(
                friendList=lFriendList,
                friendCount=len(lFriendList),
                groupList=lGroupList,
                groupCount=len(lGroupList)

            )
            return APIReturn(status=True, data=data)
        except SQLAlchemyError as se:
            return APIReturn(status=False, errorCode="0x0000000202", message=str(se.__dict__['orig']))
        except Exception as e:
            print(e)
            return APIReturn(status=False, errorCode="0x0000000203", message=e.toString())
