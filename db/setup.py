import sqlite3
from sqlite3 import Error
import logging
from db import queries

from .connection import create_conn

def setup_db(action):
    conn = create_conn()
    if action == 'create':
        sql = queries.create_table
    elif action == 'delete':
        sql = queries.delete_table
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return True
    except Error as e:
        logging.warning("Error in {} function: {}".format(action, e))
        return False
    finally:
        if conn:
            cur.close()
            conn.close()
