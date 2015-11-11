# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import uuid
import psycopg2
import unittest
from colour_runner import runner as crunner
from datetime import datetime
from mypleasure import settings
from mypleasure.tars import Tars
from mypleasure.utils import Logger

'''
Test suite for TARS
===================

None of those tests use mocks. It may raise some eyebrows, especially since
these tests end up hitting a database or calling third parties through the
wire, making the suite depending to unwiedly sources and thus, rather brittle.

But the reason I don't mock is because unit/integration tests are supposed to
improve my designs and ensure nothing brakes if I change something.
I need my tests to document how to use the system and break when set as close
as possible to production setup. White box testing is hurting my needs.

The `#noqa` comments next to some methods is to prevent my current PEP8
linter to frown at camel case method names.
'''


class MyPleasureTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyPleasureTestCase, self).__init__(*args, **kwargs)
        self.log = Logger(verbosity=0, reporting=0)
        try:
            conn_str = 'dbname={0} user={1} password={2} host={3}'.format(
                settings.TESTING_DB_NAME, settings.TESTING_DB_USER,
                settings.TESTING_DB_PASSWORD, settings.TESTING_DB_HOST
            )
            self.conn = psycopg2.connect(conn_str)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError, e:
            print '\n[TARS] Database error: %s' % e
            sys.exit(1)

    def setUp(self): # noqa
        try:
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS mediaqueue(
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
            print '\n[TARS] Database Error: %s' % e
            sys.exit(1)

    def tearDown(self): # noqa
        try:
            self.cur.execute('''TRUNCATE mediaqueue''')
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print '\n[TARS] Database Error: %s' % e
            sys.exit(1)
        finally:
            self.conn.close()

    def insert_in_mediaqueue(self, hash, url, req_id, collection_id, status):
        try:
            self.cur.execute(
                'INSERT INTO mediaqueue(hash, url, requester, collection_id, \
                status, created_at) VALUES(%s, %s, %s, %s, %s, %s)',
                (
                    hash, url, req_id, collection_id, status,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            )
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print '\n[TARS] Database Error: %s' % e
            sys.exit(1)

    def get_from_mediaqueue(self, hash):
        try:
            self.cur.execute(
                'SELECT hash, status FROM mediaqueue WHERE hash = %s LIMIT 1',
                (hash,)
            )
            results = self.cur.fetchall()
            return (
                len(results) == 1
                and results[0]
                or None
            )
        except psycopg2.DatabaseError, e:
            if self.cur:
                self.conn.rollback()
            print '\n[TARS] Database Error: %s' % e
            sys.exit(1)


class YoutubeFailureReturnsNone(MyPleasureTestCase):

    def runTest(self): # noqa
        url = 'http://youtube.com/fake'
        hash = str(uuid.uuid4())
        self.insert_in_mediaqueue(hash, url, 1, 1, 'pending')

        tars = Tars(db=self.cur)
        job = {
            'hash': hash,
            'url': url,
            'requester': 1,
            'collection_id': 1,
            'status': 'pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        result = tars.run(job, verbosity=0, reporting=0)

        self.assertIs(result, None)


class YoutubeFailureMarksStatusAsFailed(MyPleasureTestCase):

    def runTest(self): # noqa
        url = 'http://youtube.com/fake'
        hash = str(uuid.uuid4())
        self.insert_in_mediaqueue(hash, url, 1, 1, 'pending')

        tars = Tars(db=self.cur)
        job = {
            'hash': hash,
            'url': url,
            'requester': 1,
            'collection_id': 1,
            'status': 'pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        tars.run(job, verbosity=0, reporting=0)
        row = self.get_from_mediaqueue(hash)

        self.assertTupleEqual(row, (hash, 'failed'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(YoutubeFailureReturnsNone())
    suite.addTest(YoutubeFailureMarksStatusAsFailed())
    return suite


if __name__ == '__main__':
    runner = crunner.ColourTextTestRunner()
    suite = suite()
    runner.run(suite)
