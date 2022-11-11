import sqlite3
from sqlite3 import Error
import logging
from config import ConfigEnv

# Logs Config
logging.basicConfig(filename='logs/mmind.log',
                format='%(levelname)s %(asctime)s: %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
                level=ConfigEnv())

def create_conn():
    conn = None

    try:
        conn = sqlite3.connect('db/plays.db')
    except Error as e:
        logging.warning("Error connecting database: {}".format(e))
    return conn