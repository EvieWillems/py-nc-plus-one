import pytest
import os
import psycopg2
from fastapi.testclient import TestClient
from fastapi import HTTPException
from exceptions.exceptions import InvalidLoginException
import jwt


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
        'email':'no_one@nowhere.not'
    }

    response = client.post('/auth/login',json=invalid_login_attempt)
    
    assert response.status_code == 400
    assert response.json()['error'] == 'incomplete credentials'
    assert response.json()['detail'] == 'email or password not supplied'

    invalid_login_attempt = {
            'password':'not_a_password'
    }

    assert response.status_code == 400
    assert response.json()['error'] == 'incomplete credentials'
    assert response.json()['detail'] == 'email or password not supplied'