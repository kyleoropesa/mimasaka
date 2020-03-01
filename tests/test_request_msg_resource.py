from mimasaka import create_app
from assertpy import assert_that
from uuid import uuid4
import pytest


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_post_request():
    return {
        "method": "GET",
        "request_body": {
            "Test": "Lorem Ipsum Dolor"
        },
        "uri_path": "/i/am/the/pogi",
        "request_headers": {
            "Content-Type": "application/json"
        }
    }



def test_post_request_valid_values(client):
    req_body = {
        "method": "GET",
        "request_body": {
            "Test": "Lorem Ipsum Dolor"
        },
        "uri_path": "/i/am/the/pogi",
        "request_headers": {
            "Content-Type": "application/json"
        }

    }

    response = client.post('/__admin__/request', json=req_body)
    json_response = response.get_json()
    assert_that(response.status_code).is_equal_to(201)
    assert_that(json_response['id']).is_not_empty()
    assert_that(json_response['method']).is_equal_to(req_body['method'])
    assert_that(json_response['request_body']).is_equal_to(req_body['request_body'])
    assert_that(json_response['uri_path']).is_equal_to(req_body['uri_path'])
    assert_that(json_response['request_headers']).is_equal_to(req_body['request_headers'])
    assert_that(json_response['created_at']).is_not_empty()


def test_post_request_with_missing_required_fields(client):
    req_body = {
        "request_body": {
            "this": "is",
        },
        "request_headers": {
            "this": "is",
        }
    }

    response = client.post('/__admin__/request', json=req_body)
    json_response = response.get_json()
    assert_that(response.status_code).is_equal_to(400)
    assert_that(json_response['method'][0]).is_equal_to('Missing data for required field.')
    assert_that(json_response['uri_path'][0]).is_equal_to('Missing data for required field.')


def test_post_request_when_required_fields_are_only_present(client):
    req_body = {
        "method": "GET",
        "uri_path": "/i/am/the/pogi"
    }

    response = client.post('/__admin__/request', json=req_body)
    json_response = response.get_json()
    assert_that(response.status_code).is_equal_to(201)
    assert_that(json_response['id']).is_not_empty()
    assert_that(json_response['method']).is_equal_to(req_body['method'])
    assert_that(json_response['uri_path']).is_equal_to(req_body['uri_path'])
    assert_that(json_response['created_at']).is_not_empty()
    assert_that(json_response).does_not_contain_key('request_body')
    assert_that(json_response).does_not_contain_key('request_headers')


def test_post_request_for_invalid_uri_path(client):
    req_body = {
        "method": "GET",
        "request_body": {
            "Test": "Lorem Ipsum Dolor"
        },
        "uri_path": "/i/am/the/pogi",
        "request_headers": {
            "Content-Type": "application/json"
        }

    }

    response = client.post('/__admin__/requestxxx', json=req_body)
    assert_that(response.status_code).is_equal_to(404)
    assert_that(str(response.data)).contains('The requested URL was not found on the server')


def test_post_request_with_content_type_not_set_to_application_json(client):
    req_body = {
        "method": "GET",
        "request_body": {
            "Test": "Lorem Ipsum Dolor"
        },
        "uri_path": "/i/am/the/pogi",
        "request_headers": {
            "Content-Type": "application/json"
        }
    }

    response = client.post('/__admin__/request', data=req_body)
    assert_that(response.status_code).is_equal_to(400)
    assert_that(str(response.data)).contains('Invalid input type.')

def test_get_record_using_valid_record_id(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    fetched_record = client.get(f'/__admin__/request/{created_record.get_json()["id"]}', json={})
    assert_that(created_record.get_json()).is_equal_to(fetched_record.get_json())
    assert_that(fetched_record.status_code).is_equal_to(200)

def test_get_record_using_non_existing_record_id(client):
    fetched_record = client.get(f'/__admin__/request/{str(uuid4())}', json={})
    assert_that(fetched_record.status_code).is_equal_to(404)

def test_put_request_using_valid_values(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    put_request = valid_post_request
    put_request['method'] = 'PUT'
    put_request['request_body'] = {"Tested": "One Punch!!!!!!"}
    put_response = client.put(f'/__admin__/request/{created_record_json["id"]}', json=put_request)
    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(put_response.status_code).is_equal_to(200)
    assert_that(created_record_json).is_not_equal_to(updated_record_json)
    assert_that(updated_record_json['method']).is_equal_to('PUT')
    assert_that(updated_record_json['request_body']).is_equal_to({"Tested": "One Punch!!!!!!"})

def test_put_request_but_required_fields_are_missing(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    put_request = valid_post_request
    put_request.pop("method")
    put_request.pop("uri_path")
    put_response = client.put(f'/__admin__/request/{created_record_json["id"]}', json=put_request)
    put_response_json = put_response.get_json()
    assert_that(put_response.status_code).is_equal_to(400)
    assert_that(put_response_json['uri_path'][0]).is_equal_to("Missing data for required field.")
    assert_that(put_response_json['method'][0]).is_equal_to("Missing data for required field.")
    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(updated_record_json).is_equal_to(created_record_json)

def test_put_request_but_required_fields_only(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    put_request = valid_post_request
    put_request.pop("request_body")
    put_request.pop("request_headers")
    put_response = client.put(f'/__admin__/request/{created_record_json["id"]}', json=put_request)
    assert_that(put_response.status_code).is_equal_to(200)

    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(updated_record_json).is_equal_to(put_request)

def test_put_request_using_random_id(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    put_request = valid_post_request
    put_request.pop("request_body")
    put_request.pop("request_headers")
    put_response = client.put(f'/__admin__/request/{str(uuid4())}', json=put_request)
    assert_that(put_response.status_code).is_equal_to(404)

    fetched_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    fetched_record_json = fetched_record.get_json()
    assert_that(fetched_record_json).is_equal_to(created_record_json)

def test_patch_request_using_valid_values(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    patch_request = {"method": "PATCH"}
    patch_response = client.patch(f'/__admin__/request/{created_record_json["id"]}', json=patch_request)
    assert_that(patch_response.status_code).is_equal_to(200)
    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(updated_record_json).is_not_equal_to(created_record_json)
    assert_that(updated_record_json["method"]).is_equal_to(patch_request["method"])

def test_patch_request_using_multiple_valid_fields(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    patch_request = {"method": "PATCH", "request_body": {"PATCH": "Hello I'm Patch"}}
    patch_response = client.patch(f'/__admin__/request/{created_record_json["id"]}', json=patch_request)
    assert_that(patch_response.status_code).is_equal_to(200)
    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(updated_record_json).is_not_equal_to(created_record_json)
    assert_that(updated_record_json["method"]).is_equal_to(patch_request["method"])
    assert_that(updated_record_json["request_body"]).is_equal_to(patch_request["request_body"])

def test_patch_request_using_multiple_invalid_fields(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    patch_request = {"methodx": "PATCH", "request_bodyx": {"PATCH": "Hello I'm Patch"}}
    patch_response = client.patch(f'/__admin__/request/{created_record_json["id"]}', json=patch_request)
    assert_that(patch_response.status_code).is_equal_to(400)
    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(updated_record_json).is_equal_to(created_record_json)

def test_patch_request_using_empty_request_body(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    patch_response = client.patch(f'/__admin__/request/{created_record_json["id"]}', json={})
    assert_that(patch_response.status_code).is_equal_to(204)
    updated_record = client.get(f'/__admin__/request/{created_record_json["id"]}')
    updated_record_json = updated_record.get_json()
    assert_that(updated_record_json).is_equal_to(created_record_json)

def test_delete_requests_removes_item_in_storage(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    delete_response = client.delete(f'/__admin__/request/{created_record_json["id"]}')
    assert_that(delete_response.status_code).is_equal_to(200)
    get_response = client.get(f'/__admin__/request/{created_record_json["id"]}')
    assert_that(get_response.status_code).is_equal_to(404)

def test_delete_requests_removes_item_in_storage_using_non_existing_id(client, valid_post_request):
    created_record = client.post('/__admin__/request', json=valid_post_request)
    created_record_json = created_record.get_json()
    delete_response = client.delete(f'/__admin__/request/{str(uuid4())}')
    assert_that(delete_response.status_code).is_equal_to(200)
    get_response = client.get(f'/__admin__/request/{created_record_json["id"]}')
    get_response_json = get_response.get_json()
    assert_that(get_response.status_code).is_equal_to(200)
    assert_that(get_response_json).is_equal_to(created_record_json)