import pytest
import os
import psycopg2
from fastapi.testclient import TestClient
from fastapi import HTTPException

from db.connection import get_connection
from seed import seed, setup_table_structure, erd_structure_dict

def test_get_events_returns_correct_json_format(client):
    response = client.get('/events').json()
    assert isinstance(response, dict)
    assert isinstance(response['events'], list)
    assert isinstance(response['events'][0], dict)

def test_get_events_returns_all_seeded_events(client):
    response = client.get('/events').json()
    assert len(response['events']) == 5

def test_get_single_event_by_id_returns_correct_json_format(client):
    response = client.get('/events/1').json()
    assert isinstance(response, dict)
    assert isinstance(response['event'], list)
    assert isinstance(response['event'][0], dict)

def test_get_single_event_by_id_returns_correct_event_and_status_code(client):
    response = client.get('/events/1')
    expected_event = {
                        "id": 1,
                        "title": "event_d",
                        "description": "description_d",
                        "starts_at": "2026-02-02T10:00:00+00:00",
                        "ends_at": "2026-02-02T11:00:00+00:00",
                        "location": "venue_a",
                        "address": "address_a",
                        "capacity": 10
                        }
    
    for k,v in expected_event.items():
        assert response.json()['event'][0][k] == v
    assert response.status_code == 200

def test_get_single_event_by_id_raises_correct_exception_for_nonexistent_id(client):
    response = client.get('/events/99')
    assert response.status_code == 404
    assert response.json()['detail'] == 'event_id not found'

def test_get_single_event_by_id_raises_correct_exception_for_non_integer(client):
    response = client.get('/events/aardvaark')
    assert response.status_code == 400
    assert response.json()['detail'] == 'aardvaark is not a valid integer'