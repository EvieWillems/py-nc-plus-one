import psycopg2
import dotenv
from dotenv import load_dotenv
import os




def get_connection():
    '''Takes a .env filepath and returns a db connection'''
    ENV = os.getenv("ENV","development")
    dotenv.load_dotenv(f'.env.{ENV}')
    if os.getenv("PGDATABASE"):
        connection = psycopg2.connect()
        return connection
    else:
        raise RuntimeError("PGDATABASE not set")