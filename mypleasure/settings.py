# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv

try:
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
except:
    # TODO log: .env not found
    pass

DB_NAME = os.environ.get('DB_NAME', '')
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', '')
TESTING_DB_NAME = os.environ.get('TESTING_DB_NAME', '')
TESTING_DB_USER = os.environ.get('TESTING_DB_USER', '')
TESTING_DB_PASSWORD = os.environ.get('TESTING_DB_PASSWORD', '')
TESTING_DB_HOST = os.environ.get('TESTING_DB_HOST', '')
DB_TABLE_STORE = os.environ.get('DB_TABLE_STORE', '')
DB_TABLE_QUEUE = os.environ.get('DB_TABLE_QUEUE', '')

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '')

EMAIL_SMTP_SERVER = os.environ.get('EMAIL_SMTP_SERVER', '')
EMAIL_SMTP_PORT = os.environ.get('EMAIL_SMTP_PORT', '')
EMAIL_SMTP_RECIPIENT = os.environ.get('EMAIL_SMTP_RECIPIENT', '')
EMAIL_SMTP_USER = os.environ.get('EMAIL_SMTP_USER', '')
EMAIL_SMTP_PWD = os.environ.get('EMAIL_SMTP_PWD', '')

SLACK_API_KEY = os.environ.get('SLACK_API_KEY', '')
SLACK_CHAT_ROOM = os.environ.get('SLACK_CHAT_ROOM', '')

DEBUG_LOG_FILE = os.environ.get('DEBUG_LOG_FILE')
ERROR_LOG_FILE = os.environ.get('ERROR_LOG_FILE')
LOG_FILE_WRITE_MODE = os.environ.get('LOG_FILE_WRITE_MODE')
LOG_FILE_MAX_BYTES = os.environ.get('LOG_FILE_MAX_BYTES')
LOG_FILE_BACKUP_COUNT = os.environ.get('LOG_FILE_BACKUP_COUNT')
