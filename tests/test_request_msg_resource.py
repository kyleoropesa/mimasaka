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

