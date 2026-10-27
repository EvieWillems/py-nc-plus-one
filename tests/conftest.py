import pytest
import os
import psycopg2
from fastapi.testclient import TestClient
from fastapi import HTTPException
os.environ['ENV'] = 'testing'
from main import app
from db.connection import get_connection
from db.seed import seed, setup_table_structure, erd_structure_dict



@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def cursor():
    return get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor)

@pytest.fixture
def teardown_and_setup_empty():
    for t,s in erd_structure_dict.items():
        setup_table_structure(t,s)

@pytest.fixture
def full_seed():
    seed()

@pytest.fixture
def event_1():
    return {
            "id": 1,
            "title": "event_d",
            "description": "description_d",
            "starts_at": "2026-02-02T10:00:00+00:00",
            "ends_at": "2026-02-02T11:00:00+00:00",
            "organiser_id": 1,
            "venue_id": 3}
        
@pytest.fixture
def rsvp_1():
    return {"id": 1, "attendee_id": 2, "event_id": 1}
        
@pytest.fixture
def user_1():
    return {
            "name": "user_c",
            "email": "user_c@example.com",
            "password": "password_c"
            }


@pytest.fixture
def venue_1():
    return {
            "name": "venue_b",
            "address": "address_b",
            "capacity": 50
            }