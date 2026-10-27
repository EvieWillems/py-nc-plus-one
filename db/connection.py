import psycopg2
from psycopg2.extras import DictCursor
import dotenv
from dotenv import load_dotenv
import os




def get_connection():
    '''Takes a .env filepath and returns a db connection'''
    ENV = os.getenv("ENV","development")
    print(ENV)
    dotenv.load_dotenv(f'.env.{ENV}')
    db = os.getenv("PGDATABASE")
    if db:
        connection = psycopg2.connect(dbname=db)
        return connection
    else:
        raise RuntimeError("PGDATABASE not set")