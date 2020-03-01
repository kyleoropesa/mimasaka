from flask_restful import Resource
from flask import request
from marshmallow import Schema, fields
from marshmallow import ValidationError
from datetime import datetime
import uuid


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
        request_message = self.get_id_in_data_store(id)
        if request_message:
            return request_message, 200
        else:
            return {}, 404

    def post(self):
        content = request.get_json()
        serializer = RequestMessageSchema(exclude=['id', 'created_at'])
        try:
            result = serializer.load(content)
            id = str(uuid.uuid4())
            created_at = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            result['id'] = id
            result['created_at'] = created_at
            data_store[id] = result
            return result, 201
        except ValidationError as err:
            return err.messages, 400

    def put(self, id):
        content = request.get_json()
        serializer = RequestMessageSchema(exclude=['id', 'created_at'])
        request_message = self.get_id_in_data_store(id)
        try:
            result = serializer.load(content)
            if request_message:
                data_store[id] = result
                return result, 200

            return None, 404
        except ValidationError as err:
            return err.messages, 400

    def delete(self, id):
        data_store.pop(id)
        return {}, 200

    def patch(self, id):
        content = request.get_json()
        request_message = self.get_id_in_data_store(id)
        deserializer = RequestMessageSchema(exclude=['id', 'created_at'], partial=True)
        if request_message:
            try:
                result = deserializer.load(content)
                for keys in result.keys():
                    request_message[keys] = result[keys]
                data_store[id] = request_message
                return request_message, 200
            except ValidationError as err:
                return err.messages, 400

    def get_id_in_data_store(self, id):
        return data_store.get(id, None)
