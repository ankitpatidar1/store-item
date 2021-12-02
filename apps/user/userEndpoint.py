from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from apps.user.user import User


class UserApi(Resource):
    def post(self):
        data = request.get_json()
        name_pass = list(data.values())
        print('UserApi',list(data.values()))
        User().create_row(*name_pass)
        return {"status":"user added in database"}
