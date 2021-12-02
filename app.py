# from flask import Flask , render_template

# app = Flask(__name__)

# store = [{
#     "name": "Paras kirana store"
#     "items":[
#         {"name":"Soup","price":10.00},
#         {"name":"bar","price":30.00}
#         ]
# }]

# @app.route('/')
# def home():
#     return render_template('index.html')
    
# @app.route('/store' , methods=['GET'])
# def get_stores():


# @app.route('/store' , methods=['POST'])
# def create_store(data):
#     pass

# @app.route('/store/<string:name>' , methods=['POST'])
# def update_store(id, data):
#     pass

# @app.route('/store/<string:name>' , methods=['GET'])
# def get_store(id):
#     pass

# @app.route('/store/<string:name>' , methods=['DELETE'])
# def delete_store(id):
#     pass

# app.run(port=5000)

from flask import Flask ,request
from flask_restful import Resource, Api
from flask_jwt import JWT , jwt_required
from apps.user.security import authenticate,identity
from apps.store.item import Item, ItemList
from apps.store.store import Store, StoreList , storeItem
from apps.user.userEndpoint import UserApi

app = Flask(__name__)
app.secret_key = "jose"

api = Api(app)

jwt = JWT(app,authenticate,identity)

# api.add_resource(ItemList,'/item')
# api.add_resource(Item,'/item/<string:name>')

api.add_resource(UserApi,'/user') # done
api.add_resource(Store,'/store', endpoint='add_store')
api.add_resource(Store,'/store/<int:store_id>',endpoint='store')
api.add_resource(StoreList,'/stores')
api.add_resource(storeItem,'/store/<int:store_id>/items')
api.add_resource(Item,'/store/<int:store_id>/item/<int:item_id>',endpoint='item')
api.add_resource(Item,'/store/<int:store_id>/item',endpoint='add_item')
api.add_resource(ItemList,'/items')

app.run(port=6000, debug=True)