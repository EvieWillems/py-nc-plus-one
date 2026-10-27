import pytest
import os
import psycopg2
from fastapi.testclient import TestClient

from db.connection import get_connection
from db.seed import seed, setup_table_structure, erd_structure_dict

def test_get_events_returns_correct_json_format(client):
    response = client.get('/events').json()
    assert isinstance(response, dict)
    assert isinstance(response['events'], list)
    assert isinstance(response['events'][0], dict)

def test_get_events_returns_all_seeded_events(client):
    response = client.get('/events').json()
    assert len(response['events']) == 5