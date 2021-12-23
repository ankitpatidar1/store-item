from ma import ma
from apps.user.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ('password',)
        dump_only = ('id','activated',)
