from flask import g , url_for,request
from test_flask import function_accessing_global
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from flask_restful import Resource
from apps.user.user import User 
from oa import github


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        g.token = "Test Token"
        function_accessing_global()
        return github.authorize(callback=url_for("github.authorize",_external=True))


class GithubAutherize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()
        if resp is None or resp.get('access_token') is None:
            return {"message" : 'Access denied: reason=%s error=%s resp=%s' % (
                request.args['error'],
                request.args['error_description'],
                resp
            )}
        g.access_token = resp['access_token']
        github_user = github.get('user')
        github_username =  github_user.data['login']
        github_email = github_user.data['email']
        user = User.find_by_username(github_username)
        if not user:
            user = User(username=github_username,password=None, email=github_email, activated=True)
            user.create_row()

        access_token = create_access_token(identity = user.id,fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        # return github_username
        