import pytest
import os
import psycopg2

from db.connection import get_connection
from db.seed import seed, setup_table_structure, erd_structure_dict

os.environ['ENV'] = 'testing'

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
        "title": "Leeds Tech Meetup – June Edition",
        "description": "Monthly meetup for Leeds-based developers. Lightning talks and networking.",
        "starts_at": "2026-06-18T18:30:00+01:00",
        "ends_at": "2026-06-18T21:00:00+01:00",
        "organiser_id": 1,
        "venue_id": 1
        }

@pytest.fixture
def rsvp_1():
    return { "attendee_id": 2, "event_id": 1 }
        
@pytest.fixture
def user_1():
    return {
        "name": "Alice Rahman",
        "email": "alice@example.com",
        "password": "password123"
        }

@pytest.fixture
def venue_1():
    return {
    "name": "Nexus, University of Leeds",
    "address": "Discovery Way, Leeds, LS2 3AA",
    "capacity": 200
  }


def test_seed_sets_up_table_structure(cursor,teardown_and_setup_empty):
    errors_list = []
    for t in erd_structure_dict.keys():
        try:
            cursor.execute(f"SELECT * FROM {t};")
        except psycopg2.Error as e:
            errors_list.append(e)
    cursor.close()
    assert errors_list == []
    

def test_full_seed_populates_with_test_values(cursor,full_seed,event_1,rsvp_1,user_1,venue_1):
    cursor.execute('SELECT * FROM events LIMIT 1')
    sample_event = dict(cursor.fetchone())
    assert event_1 == sample_event

    cursor.execute('SELECT * FROM rsvps LIMIT 1')
    sample_rsvp = dict(cursor.fetchone())
    assert event_1 == sample_rsvp

    cursor.execute('SELECT * FROM users LIMIT 1')
    sample_user = dict(cursor.fetchone())
    assert event_1 == sample_user

    cursor.execute('SELECT * FROM venues LIMIT 1')
    sample_venue = dict(cursor.fetchone())
    assert event_1 == sample_venue