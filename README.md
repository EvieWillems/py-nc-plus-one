

## Setup and establishing db connection

db/setup.sql and db/test_setup.sql drop and setup their respective databases; run using psql if a complete reset is needed.

seed.py clears, structures and populates the db from sample development data, if run as __main__. It does this by reading erd_structure_dict, a dictionary that encodes the structure of the tables in the db. If the db structure is updated, erd_structure_dict will need to be updated accordingly.

To connect to db: create a .env file (see example). Setup filepath using os.environ['ENV'] = .env suffix (e.g.:".example" gets ".env.example"). .env file contains environment variables that provide database connection credentials. Invoke get_connection from db/connection.py to return connection object. Alternatively, invoke dict_cursor from db/connection.py as a shortcut to get a psycopg dictionary cursor factory.


## Testing

The test suite contains the following fixtures:



Each test file contains a dummy test at the start that uses the full_seed fixture to reset the db.