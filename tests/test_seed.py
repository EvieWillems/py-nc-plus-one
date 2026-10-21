import pytest
import os
import psycopg2

from db.connection import get_connection
from db.seed import seed, setup_table_structure, erd_structure_dict


@pytest.fixture
def cursor():
    return get_connection().cursor()

@pytest.fixture
def teardown_and_setup_empty():
    for t,s in erd_structure_dict.items():
        setup_table_structure(t,s)

@pytest.fixture
def full_seed():
    seed()


def test_seed_sets_up_table_structure(cursor,teardown_and_setup_empty):
    errors_list = []
    for t in erd_structure_dict.keys():
        try:
            cursor.execute(f"SELECT * FROM {t};")
        except psycopg2.Error as e:
            errors_list.append(e)
    cursor.close()
    assert errors_list == []
    

