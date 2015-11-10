# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import psycopg2
import unittest
from datetime import datetime
from psycopg2.extensions import AsIs
from mypleasure import settings
from mypleasure.tars import Tars


class MyPleasureTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyPleasureTestCase, self).__init__(*args, **kwargs)
        try:
            conn_str = 'dbname={0} user={1} password={2} host={3}'.format(
                settings.TESTING_DB_NAME, settings.TESTING_DB_USER,
                settings.TESTING_DB_PASSWORD, settings.TESTING_DB_HOST
            )
            self.conn = psycopg2.connect(conn_str)

            # Mandatory to drop database.
            self.conn.set_isolation_level(0)

            self.cur = self.conn.cursor()

            self.cur.execute(
                'DROP DATABASE {0}'.format(settings.TESTING_DB_NAME)
            )
            self.conn.commit()
            print(
                '\n[TARS] Connecting to database {0}\n.'.format(
                    settings.TESTING_DB_NAME
                )
            )
        except psycopg2.DatabaseError, e:
            print '\n[TARS] Database error: %s' % e
            sys.exit(1)

    def setUp(self):
        try:
            self.cur.execute(
                '''CREATE TABLE mediaqueue(
                id SERIAL PRIMARY KEY,
                hash VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                requester INTEGER NOT NULL,
                collection_id INTEGER NOT NULL,
                status VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)'''
            )
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print 'DB Error %s' % e
            sys.exit(1)


class MediaQueueTestCase(MyPleasureTestCase):

    def insert_in_mediaqueue(self, hash, url, req_id, collection_id, status):
        try:
            self.cur.execute(
                'INSERT INTO mediaqueue( \
                    hash, url, requester, collection_id, status, created_at \
                ) values( \
                    "%(hash)s", \
                    "%(url)s", \
                    "%(requester)s", \
                    "%(collection_id)s", \
                    "%(status)s", \
                    "%(now)s" \
                )',
                {
                    'hash': hash,
                    'url': url,
                    'requester': req_id,
                    'collection_id': collection_id,
                    'status': status,
                    'now': AsIs(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                }
            )
            self.conn.commit()
            self.cur.close()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print 'DB Error %s' % e
            sys.exit(1)

    def get_from_mediaqueue(self, hash):
        try:
            self.cur.execute(
                'SELECT * FROM mediaqueue where hash = %(hash)s',
                {'hash': hash}
            )
            return len(self.cur.fetchall()) > 0 and self.cur.fetchall() or None
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print 'DB Error %s' % e
            sys.exit(1)

    def test_failure_marks_status_as_failure(self):
        url = 'http://youtube.com/fake'
        self.insert_in_mediaqueue(
            'hash', url, 1, 1, 'pending'
        )
        tars = Tars(db=self.cur)
        result = tars.run(None, url=url)
        print(result)


if __name__ == '__main__':
    unittest.main()
