from flask import Flask, Blueprint
from flask_restful import Api
from resources.requestmessage import RequestMessage

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api_blueprint = Blueprint('api', __name__)
    api = Api(api_blueprint)

    api.add_resource(RequestMessage, '/__admin__/request/<string:id>', '/__admin__/request')
    app.register_blueprint(api_blueprint)

    return app