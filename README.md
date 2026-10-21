
To refresh test database: psql -f db/setup.sql

To connect to db: create .env file (see example). Setup filepath using os.environ['ENV'] = .env suffix (e.g.:".example" gets ".env.example"). .env file contains.database name. Invoke get_connection from db/connection.py to return connection object.