from fastapi import APIRouter, HTTPException, Depends, Request
from db.connection import get_connection, dict_cursor
import psycopg2
from utils.utils import response_formatter, response_formatter_args, compose_sql_insert
from security.user_authentication import authenticate_user
from exceptions.exceptions import RSVPConflictException
import jwt


router = APIRouter(prefix='/events')


@router.get('')
@response_formatter
def get_all_events():
    # with get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    with dict_cursor() as cursor:
        cursor.execute('SELECT ' \
                        'events.id, ' \
                        'events.title, ' \
                        'CAST(events.starts_at AS TEXT), ' \
                        'CAST(events.ends_at AS TEXT), ' \
                        'venues.name AS location '\
                        'FROM events ' \
                        'INNER JOIN venues ON events.venue_id=venues.id ' \
                        'ORDER BY events.id;')
        response = cursor.fetchall()
        return 'events',response

    
@router.get('/{event_id}')
def get_single_event_by_id(event_id):
    try:
        int(event_id)
    except:
        raise HTTPException(status_code=400,
                                detail=f'{event_id} is not a valid integer')
    with dict_cursor() as cursor:         
        cursor.execute('SELECT ' \
                        'events.id, ' \
                        'events.title, ' \
                        'events.description, ' \
                        'events.starts_at, ' \
                        'events.ends_at, ' \
                        'venues.name AS location, ' \
                        'venues.address, ' \
                        'venues.capacity, ' \
                        'events.created_at ' \
                        'FROM events ' \
                        'INNER JOIN venues ON events.venue_id=venues.id ' \
                        'WHERE events.id = %s;',(event_id,))
        response = cursor.fetchall()
        if len(response) > 0:
            return response_formatter_args('event',response)
        else:
            raise HTTPException(status_code=404,detail='event_id not found')


@router.post('/:{event_id}/rsvp')
def create_new_rsvp_for_user(event_id:int, user_id:int=Depends(authenticate_user)):
    
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute('SELECT * FROM events WHERE id = %s;',(event_id,)) == 0
            if len(cursor.fetchall()) == 0:
                raise HTTPException(status_code=404,detail='event_id not found')
            cursor.execute(*compose_sql_insert('rsvps',{'attendee_id':user_id,'event_id':event_id}))
            cursor.execute('SELECT * FROM rsvps WHERE attendee_id = %s AND event_id = %s;',(user_id,event_id))
            response = cursor.fetchall()
            if len(response) > 1:   # db doesn't have uniqueness restriction on rsvps, so test if user has already rsvpd
                raise RSVPConflictException(event_id=event_id)
            else:
                conn.commit()

    return response_formatter_args('rsvp',response)
                    