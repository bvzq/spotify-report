"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template
import connexion
#from flask_swagger_ui import get_swaggerui_blueprint
#from swagger_ui import api_doc






app = connexion.App(__name__, specification_dir="./")
app.add_api("stockify.yml")



#api_doc(app, config_path='./config/test.yaml', oauth2_config=oauth2_config)
#get_token()

# create the application instance


# Cead the swagger.yml file to configure the endpoints



# Create a URL route in our application for "/"
@app.route("/v1/api")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")

@app.route('/v1/api/users', methods=['POST', 'GET'], defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET'])
def index(path):
    print("HTTP {} to URL /{} received JSON {}".format(request.method, path, request.get_json()))
    return "True"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)