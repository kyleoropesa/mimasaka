from flask_restful import Resource
from marshmallow import Schema, fields


data_store = {}


class RequestMessageSchema(Schema):
    id = fields.UUID(required=True)
    method = fields.String(required=True)
    request_body = fields.Dict(required=False)
    uri_path = fields.String(required=True)
    request_headers = fields.Dict(required=False)
    created_at = fields.DateTime(required=True)


class RequestMessage(Resource):
    def get(self, id):
        pass

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def patch(self, id):
        pass
