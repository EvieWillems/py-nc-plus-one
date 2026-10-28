from fastapi import APIRouter, HTTPException
from db.connection import get_connection, dict_cursor
import psycopg2
from utils.utils import response_formatter, response_formatter_args

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