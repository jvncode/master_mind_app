import os
import logging
from dotenv import load_dotenv

load_dotenv()

# APPLICATION ENVIROMENT CONFIGURATION
APP_ENV = os.environ.get('APP_ENV', default='')
PORT = os.environ.get('PORT', default='')

# GAME CONFIG
COLORS = ['R', 'G', 'B', 'Y']

def ConfigEnv():
    if APP_ENV == 'DEV':
        return logging.DEBUG
    elif APP_ENV == 'PROD':
        return logging.WARNING
