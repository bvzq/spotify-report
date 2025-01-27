"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template
import connexion
#from flask_swagger_ui import get_swaggerui_blueprint
#from swagger_ui import api_doc



#flask_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')
oauth2_config = {
    "clientId": "\"eQ6tITxMVX1OucaDcciPpMCX9Ra7qayB\"",
    "clientSecret": "\"nUgSv4YYNDomChzr9sYLOPl70XbBmzeWxjVVRb4E9Qg5-lIKtYjsckzirpJ74PJn\"",
    "realm": "\"your-realms\"",
    "appName": "\"stockify\"",
    "scopeSeparator": "\" \"",
    "scopes": "\"['read_user']\"",
    "additionalQueryStringParams": "{test: \"hello\"}",
    "usePkceWithAuthorizationCodeGrant": True,
}

options = {"swagger_ui_config": {"initOAuth":oauth2_config }}

app = connexion.App(__name__, specification_dir="./",options=options)
app.add_api("account.yml")



#api_doc(app, config_path='./config/test.yaml', oauth2_config=oauth2_config)
#get_token()

# create the application instance


# Cead the swagger.yml file to configure the endpoints



# Create a URL route in our application for "/"
@app.route("/v1/api")
def index(path):
    print("HTTP {} to URL /{} received JSON {}".format(request.method, path, request.get_json()))
    return "True"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5002)