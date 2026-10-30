from fastapi import FastAPI, APIRouter, HTTPException, Response, status
from db.connection import get_connection, dict_cursor
import psycopg2
from psycopg2.errors import UniqueViolation
from utils.utils import response_formatter, response_formatter_args, compose_sql_insert
from schemas import NewUserProfile, LoginDetails
from security.encryption import create_access_token, verify_password
from exceptions.exceptions import InvalidLoginException, ExistingUserException
from security.encryption import hash_password
from security.user_authentication import authenticate_user

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
def create_new_user_profile(details: NewUserProfile, http_response:Response):
    credentials = dict(details)
    credentials['password'] = hash_password(credentials['password'])
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            try:
                cursor.execute(*compose_sql_insert('users',credentials))
            except UniqueViolation:
                raise ExistingUserException
            conn.commit()
            cursor.execute('SELECT id, name, email, created_at ' \
                        'FROM users ' \
                        'WHERE email = %s;',(credentials['email'],))
            response = cursor.fetchall()
            http_response.status_code = status.HTTP_201_CREATED
            return response_formatter_args('user',response)
        
