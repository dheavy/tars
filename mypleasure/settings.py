# -*- coding: utf-8 -*-


import os
from os.path import join, dirname
from dotenv import load_dotenv

try:
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
except:
    # log: .env not found
    pass

DB_NAME = os.environ.get('DB_NAME', '')
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', '')
DB_TABLE_STORE = os.environ.get('DB_TABLE_STORE', '')
DB_TABLE_QUEUE = os.environ.get('DB_TABLE_QUEUE', '')
