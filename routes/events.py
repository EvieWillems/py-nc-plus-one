from fastapi import APIRouter
from db.connection import get_connection
import psycopg2
# from psycopg2.extras import DictCursor
from decorators import response_formatter, response_formatter_args

router = APIRouter(prefix='/events')


@router.get('')
@response_formatter
def get_all_events():
    with get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT ' \
                        'events.id, ' \
                        'events.title, ' \
                        'events.starts_at, ' \
                        'events.ends_at, ' \
                        'venues.name AS location '\
                        'FROM events ' \
                        'INNER JOIN venues ON events.venue_id=venues.id ' \
                        'ORDER BY events.id;')
        response = cursor.fetchall()
        return 'events',response


@router.get('/{event_id}')
# @response_formatter_args
def get_single_event_by_id(event_id):
    with get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM events WHERE id = %s',(event_id,))
        response = cursor.fetchone()
        return 'event', response