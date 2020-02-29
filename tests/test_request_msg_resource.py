from mimasaka import create_app
from assertpy import assert_that
import pytest


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_successful_post_request(client):
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
    assert_that(response.status_code).is_equal_to(200)
    assert_that(json_response['id']).is_not_empty()
    assert_that(json_response['method']).is_equal_to(req_body['method'])
    assert_that(json_response['request_body']).is_equal_to(req_body['request_body'])
    assert_that(json_response['uri_path']).is_equal_to(req_body['uri_path'])
    assert_that(json_response['request_headers']).is_equal_to(req_body['request_headers'])


def test_error_if_method_field_is_missing_in_request_body(client):
    req_body = {
        "request_body": {
            "this": "is",
        },
        "uri_path": "/i/am/the/pogi",
        "request_headers": {
            "this": "is",
        }
    }

    response = client.post('/__admin__/request', json=req_body)
    json_response = response.get_json()
    assert_that(response.status_code).is_equal_to(400)
    assert_that(json_response['method'][0]).is_equal_to('Missing data for required field.')
