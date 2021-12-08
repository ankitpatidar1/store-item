from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from apps.user.user import User


class UserApi(Resource):
    def post(self):
        data = request.get_json()
        msg = User(data).create_row()
        return {"status":msg}

    def get(self):
        users = User().fetch()
        return {
            "users":list(
                map(
                    lambda user:{
                        "id":user.id,
                        "username":user.username,
                        "password":user.password
                    },users)) }