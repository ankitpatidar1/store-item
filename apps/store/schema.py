from ma import ma
from marshmallow import Schema, fields
from apps.store.models import StoreModel,ItemModel
from werkzeug.datastructures import FileStorage

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ('store',)
        dump_only = ('id',)
        include_fk = True

class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoreModel
        dump_only = ('id',)


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value , attr, data,**kwargs):
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            return self.fail('invalid')
        
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)
