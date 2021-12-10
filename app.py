from flask import Flask ,request ,jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager , jwt_required
from apps.store.item import Item, ItemList
from apps.store.store import Store, StoreList , storeItem
from apps.user.userEndpoint import UserApi , UserLogin , TokenRefresh , UserLogout
from db import db
from blacklist import BLACKLIST



app = Flask(__name__)
app.secret_key = "jose"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/user.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BACKLIST_ENABLED'] = True
app.config['JWT_BACKLIST_TOKEN_CHECK'] = ['access','refresh']


api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

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
# api.add_resource(ItemList,'/item')
# api.add_resource(Item,'/item/<string:name>')

api.add_resource(UserApi,'/user', endpoint='user') # done
api.add_resource(UserLogin,'/user/login') # done
api.add_resource(TokenRefresh,'/user/refresh') # done
api.add_resource(UserLogout,'/user/logout') # done

api.add_resource(UserApi,'/user/<int:user_id>',endpoint='update_user')

api.add_resource(Store,'/store', endpoint='add_store')
api.add_resource(Store,'/store/<int:store_id>',endpoint='store')
api.add_resource(StoreList,'/stores')
api.add_resource(storeItem,'/store/<int:store_id>/items')
api.add_resource(Item,'/store/<int:store_id>/item/<int:item_id>',endpoint='item')
api.add_resource(Item,'/store/<int:store_id>/item',endpoint='add_item')
api.add_resource(ItemList,'/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)