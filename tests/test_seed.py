import pytest
import os
import psycopg2

from db.connection import get_connection
from seed import seed, setup_table_structure, erd_structure_dict

# os.environ['ENV'] = 'testing'


def test_seed_sets_up_table_structure(cursor,full_seed):
    errors_list = []
    for t in erd_structure_dict.keys():
        try:
            cursor.execute(f"SELECT * FROM {t};")
        except psycopg2.Error as e:
            errors_list.append(e)
    cursor.close()
    assert errors_list == []
    

# def test_full_seed_populates_with_test_values(cursor,full_seed,event_1,rsvp_1,user_1,venue_1):
#     cursor.execute('SELECT * FROM events LIMIT 1')
#     sample_event = dict(cursor.fetchone())
#     assert event_1 == sample_event

#     cursor.execute('SELECT * FROM rsvps LIMIT 1')
#     sample_rsvp = dict(cursor.fetchone())
#     assert rsvp_1 == sample_rsvp

#     cursor.execute('SELECT * FROM users LIMIT 1')
#     sample_user = dict(cursor.fetchone())
#     assert user_1 == sample_user

#     cursor.execute('SELECT * FROM venues LIMIT 1')
#     sample_venue = dict(cursor.fetchone())
#     assert venue_1 == sample_venue