from fastapi import APIRouter, HTTPException
from db.connection import get_connection, dict_cursor
import psycopg2
from utils.utils import response_formatter, response_formatter_args
from schemas import NewUserProfile, LoginDetails
from encryption.encryption import create_access_token, verify_password

router = APIRouter(prefix='/auth')

@router.post('/login')
def user_login(details: LoginDetails):
    cursor = dict_cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s',(details.email,))
    response = cursor.fetchall()

    if verify_password(password=details.password,hashed_password=response[0]['password']):
        return create_access_token(response[0]['id'])
