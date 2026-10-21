import psycopg2
import dotenv
from dotenv import load_dotenv
import os




def get_connection():
    '''Takes a .env filepath and returns a db connection'''
    ENV = os.getenv("ENV")
    dotenv.load_dotenv(ENV)
    connection = psycopg2.connect()
    return connection