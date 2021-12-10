from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required , 
    get_jwt,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask import request
from werkzeug.security import safe_str_cmp
from apps.user.user import User
from blacklist import BLACKLIST


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


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.find_by_username(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity = user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        return {"message": "Invalid credentials"},401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {"access_token":new_token},200

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message":"Logout successfully"} , 200