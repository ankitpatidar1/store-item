from flask import Flask ,request
from flask_restful import Resource, Api
from flask_jwt import JWT , jwt_required
from apps.user.security import authenticate,identity
from apps.store.item import Item, ItemList
from apps.store.store import Store, StoreList , storeItem
from apps.user.userEndpoint import UserApi
from db import db

app = Flask(__name__)
app.secret_key = "jose"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/user.db'


api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate,identity)

# api.add_resource(ItemList,'/item')
# api.add_resource(Item,'/item/<string:name>')

api.add_resource(UserApi,'/user', endpoint='user') # done
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