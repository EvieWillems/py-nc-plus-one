from typing import Optional
from psycopg2 import sql

def response_formatter(endpoint):
    def wrapper():
        '''endpoints return tuple = (title,response), where response = ordered dict'''
        '''wrapper converts into readable json format''' 
        title_response = endpoint()
        return {title_response[0]:[dict(r) for r in title_response[1]]}
    return wrapper

def response_formatter_args(title,response):
    '''takes json dict key and ordered dict and returns readable json format'''
    return {title:[dict(r) for r in response]}

def compose_sql_insert(table,details):
    '''takes target table name and dict with keys=columns, values=insert values'''
    '''returns valid sql string, tuple with values, for passing to cursor.execute()'''
    insert_string = sql.SQL(
        'INSERT INTO {tab} ({fields}) VALUES ({values});'
                ).format(tab=sql.Identifier(table),
                         fields=sql.SQL(', ').join([sql.Identifier(k) for k in details.keys()]),
                         values=sql.SQL(', ').join([sql.Placeholder() for v in details.values()]))
    insert_tuple = tuple([v for v in details.values()])
    return insert_string, insert_tuple