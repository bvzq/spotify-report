from threading import activeCount
import account
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask import make_response,jsonify,abort
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

#from dotenv import load_dotenv, find_dotenv
from flask import redirect
from flask import session
from flask import url_for
import json
from six.moves.urllib.request import urlopen
from functools import wraps
import http.client
from flask import request, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt
#from six.moves.urllib.parse import urlencode
#from oauthlib.oauth2 import WebApplicationClient, AuthorizationCodeGrant

"""def oauth_user(request,scope):
    client_id = request.get('username')
    client = WebApplicationClient(client_id)
    url = client.prepare_request_uri(
        authorization_url = 'http:localhost:5000/v1/api/oauth/authorize',
        redirect_uri='http:localhost:5000/v1/api/users',
        scope = scope,
        state= 'D8VAo311AAl_49LAtM51HA'
    )

    data = client.prepare_request_body(
        code = AuthorizationCodeGrant().create_authorization_code(request),
        redirect_uri='http:localhost:5000/v1/api/users',
        client_id = client_id,
        client_secret = 'my_secret'

    )

    header = {
        'Authorization': 'Bearer {}'.format(client.token['access_token'])
    }
    response = request.get('http:localhost:5000/v1/api/user', headers=header)
    print(response)
    return response"""

APP = Flask(__name__)


AUTH0_DOMAIN = 'dev-ic19sbcj.us.auth0.com'
API_AUDIENCE = "https://stockify_api"
ALGORITHMS = ["RS256"]
jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
jwks = json.loads(jsonurl.read())

APP = Flask(__name__)

def get_token(token):
        
    """"unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        _request_ctx_stack.top.current_user = payload
    raise AuthError({"code": "invalid_header",
                    "description": "Unable to find appropriate key"}, 401)"""
    return token




@APP.route("/v1/api/users")
@cross_origin(headers=["Content-Type", "Authorization"])
def read_user(username):
    #response = oauth_user(request_get_user,['read_user'])
    acc_serv = account.AccountService()
    resp = acc_serv.readUser(username)
    
    if resp:
        return make_response(jsonify(
        {"birth_date":resp.birth_date,
        "email": resp.email,
        "gender": resp.gender,
        "username": resp.username,
        "votes": {"ccode":[resp.vote_history[i].ccode for i in range(len(resp.vote_history))],
                "vote_type": ['Up' if resp.vote_history[i].vote_type == 1 else 'Down' for i in range(len(resp.vote_history))]
        }}),200)
    else:
        return abort(
            404
        )
def update_user(username,request_update):
    request = {'username_default':username,'body_request':request_update}
    resp = account.AccountService().updateUser(request)
    if resp:
        return make_response(jsonify({'message':resp.message}),200)
    else:
        return abort(404)

def delete_user(username):
    resp = account.AccountService().deleteUser(username)
    if resp:
        return make_response(jsonify({'message':resp.message}),200)
    else:
        abort(404)

def create_vote(req_user_vote):
    resp = account.AccountService().createVote(req_user_vote)
    if resp:
        return make_response(jsonify({"message":resp.message}),200)
    else:
        abort(404)

def create_user(request_user):
    #print(request_user)
    acc_serv = account.AccountService()
    resp = acc_serv.createUser(request_user)
    return make_response(
            jsonify({"message": resp.message}), 201
        )


