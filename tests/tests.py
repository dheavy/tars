# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import psycopg2
import unittest
from mypleasure import settings


class MyPleasureTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyPleasureTestCase, self).__init__(*args, **kwargs)
        try:
            conn_str = 'dbname={0} user={1} password={2} host={3}'.format(
                settings.TESTING_DB_NAME, settings.TESTING_DB_USER,
                settings.TESTING_DB_PASSWORD, settings.TESTING_DB_HOST
            )
            self.conn = psycopg2.connect(conn_str)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.cur.rollback()
            print 'Error %s' % e
            sys.exit(1)

    def setUp(self):
        try:
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS mediaqueue(
                id SERIAL PRIMARY KEY,
                hash VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                requester INTEGER NOT NULL,
                collection_id INTEGER NOT NULL,
                status VARCHAR(255) NOT NULL,
                created_at TIMESTAMP)'''
            )
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.cur.rollback()
            print 'Error %s' % e
            sys.exit(1)

    def tearDown(self):
        try:
            # Mandatory to drop database.
            self.conn.set_isolation_level(0)
            self.cur.execute(
                '''DROP DATABASE IF EXISTS mediaqueue'''
            )
            self.conn.commit()
            self.cur.close()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print 'Error %s' % e
            sys.exit(1)


if __name__ == '__main__':
    unittest.main()
