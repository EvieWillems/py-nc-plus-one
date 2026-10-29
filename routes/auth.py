from fastapi import APIRouter, HTTPException
from db.connection import get_connection, dict_cursor
import psycopg2
from utils.utils import response_formatter, response_formatter_args, compose_sql_insert
from schemas import NewUserProfile, LoginDetails
from encryption.encryption import create_access_token, verify_password
from exceptions.exceptions import InvalidLoginException
from encryption.encryption import hash_password

router = APIRouter(prefix='/auth')

@router.post('/login')
def user_login(details: LoginDetails):
    with dict_cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE email = %s',(details.email,))
        response = cursor.fetchall()
        if len(response) == 0:
            raise InvalidLoginException()
        elif verify_password(password=details.password,hashed_password=response[0]['password']):
            return create_access_token(response[0]['id'])
        else:
            raise InvalidLoginException()

@router.post('/register')
def create_new_user_profile(details: NewUserProfile):
    credentials = dict(details)
    credentials['password'] = hash_password(credentials['password'])
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(*compose_sql_insert('users',credentials))
            conn.commit()
            cursor.execute('SELECT id, name, email, created_at ' \
                        'FROM users ' \
                        'WHERE email = %s;',(credentials['email'],))
            response = cursor.fetchall()

            return response_formatter_args('user',response)
        

    
