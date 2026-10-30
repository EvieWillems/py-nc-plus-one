import pytest
import os
import psycopg2
from fastapi.testclient import TestClient
from fastapi import HTTPException
from exceptions.exceptions import InvalidLoginException
import jwt
from conftest import dict_cursor_testing
from encryption.encryption import verify_password

def test_reset_db_auth(full_seed):
    pass

def test_user_login_validates_matching_credentials(client,valid_login_attempt):
    response = client.post('/auth/login',json=valid_login_attempt).json()
    assert isinstance(response,str)

def test_user_login_raises_error_for_invalid_credentials(client):

    invalid_login_attempt = {
        'email':'no_one@nowhere.not',
        'password':'not_a_password'
    }

    response = client.post('/auth/login',json=invalid_login_attempt)

    assert response.status_code == 401
    assert response.json()['error'] == 'invalid login'
    assert response.json()['detail'] == 'invalid email or password'

def test_missing_fields_raise_bad_request_exception(client):
    
    invalid_login_attempt = {
        "email": "user_c@example.com"
    }

    response = client.post('/auth/login',json=invalid_login_attempt)
    
    assert response.status_code == 400
    assert response.json()['error'] == 'incomplete credentials'
    assert response.json()['detail'] == 'email or password not supplied'

    invalid_login_attempt = {
        "password": "password_c"
    }

    response = client.post('/auth/login',json=invalid_login_attempt)

    assert response.status_code == 400
    assert response.json()['error'] == 'incomplete credentials'
    assert response.json()['detail'] == 'email or password not supplied'

def test_create_new_user_successfully_creates_new_profile_and_returns_details(client,teardown_and_setup_empty,user_1):

    expected = {
        'id':1,
        'name': 'user_c',
        'email': 'user_c@example.com'
    }

    response = client.post('/auth/register',json=user_1)

    assert response.status_code == 201

    response_json = response.json()

    assert isinstance(response_json, dict)
    assert isinstance(response_json['user'][0], dict)
    assert isinstance(response_json['user'], list)
    for f in expected.keys():
        assert expected[f] == response_json['user'][0][f]

def test_create_new_user_doesnt_return_password_in_any_form(client,teardown_and_setup_empty,user_1):

    response = client.post('/auth/register',json=user_1).json()

    for u in response['user']:
        assert not 'password' in u.keys()
        assert not user_1['password'] in u.values()



def test_created_user_password_hashed(client,teardown_and_setup_empty,user_1):

    client.post('/auth/register',json=user_1)
    with dict_cursor_testing() as cursor:
        cursor.execute('SELECT password FROM users WHERE id = 1')
        password = cursor.fetchall()[0][0]

    assert password != user_1['password']
    assert verify_password(user_1['password'],password)

def test_missing_field_in_user_creation_returns_missing_field_error(client,teardown_and_setup_empty):

    invalid_user = {
        "email": "user_c@example.com"
    }

    response = client.post('/auth/register',json=invalid_user)

    assert response.status_code == 400
    assert response.json()['error'] == 'incomplete credentials'
    assert response.json()['detail'] == 'email or password not supplied'

    invalid_user = {
            "password": "pssword_1"
        }
    
    response = client.post('/auth/register',json=invalid_user)

    assert response.status_code == 400
    assert response.json()['error'] == 'incomplete credentials'
    assert response.json()['detail'] == 'email or password not supplied'

def test_create_user_returns_error_if_email_already_exists(client,full_seed,user_1):

    response = client.post('/auth/register',json=user_1)

    assert response.status_code == 409
    assert response.json()['error'] == 'existing user'
    assert response.json()['detail'] == 'user with that email already exists'