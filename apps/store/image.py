from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
import traceback
import os
from flask_jwt_extended import jwt_required , get_jwt_identity
import image_helper
from apps.store.schema import ImageSchema

class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        data = ImageSchema().load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_helper.save_image(data['image'], folder)
            get_basename = image_helper.get_basename(image_path)
            return { "message" : "Image has uploaded file :%s" % get_basename }, 201
        except:
            extension = image_helper.get_extension(data['image'])
            return {"message": "image illage extension %s" % extension}, 400
    
    @jwt_required()
    def get(self, filename):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        # if not image_helper.is_filename_safe(filename):
        #     return {"message": "filename is not contain valid extension"}
        try:
            return send_file(image_helper.get_path(filename,folder=folder))
        except FileNotFoundError:
            return {"message": "filename does not  exist in system"}
        except Exception as e:
            traceback.print_exc()
            return {"message":e.msg}

    @jwt_required()
    def delete(self, filename):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        # if not image_helper.is_filename_safe(filename):
        #     return {"message": "filename is not contain valid extension"}
        try:
            os.remove(image_helper.get_path(filename,folder=folder))
            return {"message": "filename has been deleted successfully"}
        except FileNotFoundError:
            return {"message": "filename does not  exist in system"}
        except Exception as e:
            traceback.print_exc()
            return {"message":e.msg}

