import pytest
import os
import psycopg2
from fastapi.testclient import TestClient
from fastapi import HTTPException
from conftest import dict_cursor_testing, drop_table_and_create_empty, create_rsvp

from db.connection import get_connection
from seed import seed, setup_table_structure, erd_structure_dict

def test_reset_db_events(full_seed):
    pass

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

def test_rsvp_to_event_returns_correct_json_given_valid_token(client,valid_token):

    expected = {
        'id':1,
        'attendee_id':1,
        'event_id':1
    }

    drop_table_and_create_empty('rsvps')
    auth_headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.post('events/:1/rsvp',headers=auth_headers).json()

    assert isinstance(response,dict)
    for k in expected.keys():
        assert expected[k] == response['rsvp'][0][k]


def test_rsvp_to_event_returns_correct_error_and_status_code_given_invalid_token(client):

    expected = {'error':'invalid request','detail':'Unauthorized'}

    invalid_token = "yeJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzkzNTMzMzk3fQ.tpIQ_dGcYSXqFCLp1Lw9Paxkw8x3aK3U9mrt670SPq4"
    drop_table_and_create_empty('rsvps')
    auth_headers = {'Authorization': f'Bearer {invalid_token}'}
    response = client.post('events/:1/rsvp',headers=auth_headers)

    assert response.status_code == 401
    assert response.json() == expected


def test_rsvp_to_event_returns_correct_error_and_status_code_given_expired_token(client):

    expected = {'error':'invalid request','detail':'Unauthorized'}

    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzkzNTMzMzk3fQ.tpIQ_dGcYSXqFCLp1Lw9Paxkw8x3aK3U9mrt670SPq4"
    drop_table_and_create_empty('rsvps')
    auth_headers = {'Authorization': f'Bearer {expired_token}'}
    response = client.post('events/:1/rsvp',headers=auth_headers)

    assert response.status_code == 401
    assert response.json() == expected

def test_validated_rsvp_to_event_returns_error_when_rsvp_for_user_event_pair_already_exists(client,valid_token):
    
    expected = {'error':'rsvp conflict','detail':'user has already rsvpd to event 1'}
    
    drop_table_and_create_empty('rsvps')
    auth_headers = {'Authorization': f'Bearer {valid_token}'}
    client.post('events/:1/rsvp',headers=auth_headers)
    response = client.post('events/:1/rsvp',headers=auth_headers)

    assert response.status_code == 409
    assert response.json() == expected

def test_rsvp_for_non_existent_event_returns_correct_error_and_status_code(client,valid_token):
        
    expected = {'error':'invalid request','detail':'event_id not found'}
    drop_table_and_create_empty('rsvps')
    drop_table_and_create_empty('events')
    response = create_rsvp(client,valid_token)
    assert response.status_code == 404
    assert response.json() == expected

def test_delete_rsvp_deletes_rsvp_when_validated(client,valid_token,full_seed):

    create_rsvp(client,valid_token)
    auth_headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.delete('/events/:1/rsvp/me',headers=auth_headers)
    assert response.status_code == 204

def test_delete_rsvp_returns_unauthorized_error_with_invalid_token(client,valid_token,full_seed):

    invalid_token = "yeJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzkzNTMzMzk3fQ.tpIQ_dGcYSXqFCLp1Lw9Paxkw8x3aK3U9mrt670SPq4"
    expected = {'error':'invalid request','detail':'Unauthorized'}

    create_rsvp(client,valid_token)
    auth_headers = {'Authorization': f'Bearer {invalid_token}'}
    response = client.delete('/events/:1/rsvp/me',headers=auth_headers)

    assert response.status_code == 401
    assert response.json() == expected

def test_delete_rsvp_raises_correct_exception_when_event_doesnt_exist(client,valid_token):
        
    expected = {'error':'invalid request','detail':'event_id not found'}

    drop_table_and_create_empty('rsvps')
    drop_table_and_create_empty('events')

    response = auth_headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.delete('/events/:1/rsvp/me',headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == expected