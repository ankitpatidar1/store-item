from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required , 
    get_jwt,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask import request , make_response, render_template
from werkzeug.security import safe_str_cmp
from apps.user.user import User
from blacklist import BLACKLIST
from apps.user.schema import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class UserApi(Resource):
    
    def post(self):

        user  = UserSchema(load_instance=True).load(request.get_json())
        instance = user.create_row()
        
        # send  user confirmation mail
        user.send_confirmation()
        return user_schema.dump(instance)

    def get(self):
        users = User().fetch()
        return {"users":user_list_schema.dump(users)}


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.find_by_username(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            if user.activated:
                access_token = create_access_token(identity = user.id,fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            else:
                return {'message': "the <{}> user is not activated ".format(user.username)} , 400

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

class UserConfirm(Resource):
    @classmethod
    def get(cls,user_id: int):
        user = User.find_by_id(user_id)

        if not user:
            return {"message": "user not found"}, 404
        
        user.activated = True
        user.create_row()
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("email_confirmation.html", email=user.username),200, headers)

            