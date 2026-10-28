import pytest
import os
import psycopg2
from fastapi.testclient import TestClient
from fastapi import HTTPException
import jwt

from db.connection import get_connection
from seed import seed, setup_table_structure, erd_structure_dict

# def test_user_login_returns_valid_token_format_on_success(client,valid_login_attempt):
#     response = client.post('/auth/login',json=valid_login_attempt).json()
#     assert 

def test_user_login_validates_matching_credentials(client,valid_login_attempt):
    response = client.post('/auth/login',json=valid_login_attempt).json()
    assert response