import sqlite3
from sqlite3 import Error
import logging

from .connection import create_conn

def exec_db(sql, data=False):
    conn = create_conn()

    try:
        cur = conn.cursor()
        if data:
            action = 'Insert'
            cur.execute(sql, data)
        else:
            action = 'Get'
            cur.execute(sql)
        conn.commit()
        logging.info("{} DB".format(action))
        return cur.fetchall()
    except Error as e:
        logging.warning("Error insert at DB: {}".format(e))
        return False
    finally:
        if conn:
            cur.close()
            conn.close()


