
import sqlite3 as sql

_db_path = 'data/databases/entity.db'

def _run_sql(code):
    with sql.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(code)
        result = cursor
    return result

def add_record(record,table='entity_data'):
    keys,values = tuple(record.keys()),tuple(record.values())
    columns = ('{},'*len(keys))[:-1].format(*keys)
    values = ('\'{}\','*len(values))[:-1].format(*values)
    code = 'INSERT INTO {} ({}) VALUES ({});'.format(table,columns,values)
    _run_sql(code)

def select_record(name,table='entity_data'):
    code = f'SELECT * FROM {table} WHERE name = \'{name}\';'
    result = _run_sql(code)
    keys = [i[0] for i in result.description]
    values = result.fetchone()
    record = dict(zip(keys, values))
    return record
