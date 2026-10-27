import psycopg2
from psycopg2.errors import InFailedSqlTransaction, UndefinedTable
import os
import json

if not __name__ == '__main__':
    from db.connection import get_connection
else:
    from connection import get_connection

def seed():

    for t,s in erd_structure_dict.items():
        setup_table_structure(t,s)

    for t in erd_structure_dict.keys():
        populate_table(t)

    
        
def setup_table_structure(table, structure):

    '''Sets up table structure by looping through structured dictionary'''

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table};")

    command_string = f"CREATE TABLE {table} ("

    for column,keywords in structure.items():
        command_string += f"{column} {keywords}, "

    command_string = command_string[:-2] + ");"
    cursor.execute(command_string)

    
    if __name__ == "__main__": print(command_string)
    
    cursor.close()
    connection.commit()
    connection.close()


def populate_table(table):

    '''Reads data from files, populates tables in db by constructing insert string'''

    connection = get_connection()

    with open(f'db/data/{table}.json') as file:
        data = json.load(file)

    for entry in data:
        
        cursor = connection.cursor()
        insert_statement = f'INSERT INTO {table} ('

        for column in entry.keys():
            insert_statement += f'{column}, ' 

        insert_statement = insert_statement[:-2]+') VALUES ('

        for column in entry.keys():
            insert_statement += '%s, '

        insert_statement = insert_statement[:-2]+');'
        values = tuple([v for v in entry.values()])

        try:
            cursor.execute(insert_statement, values)
            if __name__ == '__main__':
                print(insert_statement)
                print(values)
        except:
            if __name__ == '__main__': print('failed to insert data:',end=' ')
            print(values)

        
        
        cursor.close()
        connection.commit()

    
    connection.close()


erd_structure_dict = {
    'users': {'id':'SERIAL PRIMARY KEY',
              'email':'VARCHAR(255) UNIQUE NOT NULL',
              'password':'VARCHAR(255) NOT NULL',
              'name':'VARCHAR(255) NOT NULL',
              'created_at': 'TIMESTAMPTZ DEFAULT NOW()'},
    'venues': {'id':'SERIAL PRIMARY KEY',
               'name':'VARCHAR(255) NOT NULL',
               'address':'TEXT',
               'capacity':'INT'},
    'events': {'id':'SERIAL PRIMARY KEY',
               'title':'VARCHAR(255) NOT NULL',
               'description':'VARCHAR(255) NOT NULL',
               'starts_at':'TIMESTAMPTZ NOT NULL',
               'ends_at':'TIMESTAMPTZ NOT NULL',
               'organiser_id':'INT',
               'venue_id':'INT',
               'created_at':'TIMESTAMPTZ DEFAULT NOW()'},
    'rsvps': {'id':'SERIAL PRIMARY KEY',
              'attendee_id':'INT',
              'event_id':'INT',
              'created_at':'TIMESTAMPTZ DEFAULT NOW()'}
}

os.environ['ENV'] = 'development'

seed()

