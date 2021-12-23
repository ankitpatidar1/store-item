from flask import Flask ,request ,jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager , jwt_required
from flask_uploads import  configure_uploads
from marshmallow import ValidationError
import os
from apps.store.item import Item, ItemList
from apps.store.store import Store, StoreList , storeItem
from apps.store.image import ImageUpload
from image_helper import IMAGE_SET
from apps.user.userEndpoint import (
    UserApi, 
    UserLogin,
    TokenRefresh,
    UserLogout,
    UserConfirm,
)
from db import db
from blacklist import BLACKLIST
from ma import ma

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/user.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BACKLIST_ENABLED'] = True
app.config['JWT_BACKLIST_TOKEN_CHECK'] = ['access','refresh']
app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
app.config['MAX_CONTENT_LENGTH'] = 10*1024*1024
api = Api(app)
db.init_app(app)
ma.init_app(app)
# patch_request_class(app, 10*1024*1024)
configure_uploads(app, IMAGE_SET)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)


@app.errorhandler(ValidationError)
def habdle_marshmallow_error(err):
    return jsonify(err.normalized_messages()),400

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 2:
        return { "is_admin": True }
    return { "is_admin": False }

@jwt.token_in_blocklist_loader
def check_if_token_in_backlist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

@jwt.expired_token_loader
def expried_token_callback(jwt_header, jwt_payload):
    return jsonify({"description":"The token has expried",
    "error":"Token_expried"}), 401

@jwt.unauthorized_loader
def unauthorized_user_loader():
    return jsonify(
        {
            "description":"User is not authorized",
            "error":"User_Unauthorized",
        }
    ), 401

@jwt.needs_fresh_token_loader
def token_not_refresh_callback():
    return jsonify(
        {
            "description":"The token is not fresh",
            "error":"Need_Fresh_Token",
        }
    ), 401

@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify(msg=f"I'm sorry {jwt_payload['sub']} I can't let you do that")


api.add_resource(UserApi,'/user', endpoint='user')
api.add_resource(UserLogin,'/user/login')
api.add_resource(TokenRefresh,'/user/refresh')
api.add_resource(UserLogout,'/user/logout')
api.add_resource(UserConfirm,'/user/confirm/<int:user_id>')

api.add_resource(UserApi,'/user/<int:user_id>',endpoint='update_user')

api.add_resource(Store,'/store', endpoint='add_store')
api.add_resource(Store,'/store/<int:store_id>',endpoint='store')
api.add_resource(StoreList,'/stores')
api.add_resource(storeItem,'/store/<int:store_id>/items')
api.add_resource(Item,'/store/<int:store_id>/item/<int:item_id>',endpoint='item')
api.add_resource(Item,'/store/<int:store_id>/item',endpoint='add_item')
api.add_resource(ItemList,'/items')
api.add_resource(ImageUpload,'/upload/image', endpoint="image_upload")
api.add_resource(ImageUpload,'/image/<string:filename>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)