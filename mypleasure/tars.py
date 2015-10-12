# -*- coding: utf-8 -*-
import mypleasure.settings as settings
from psycopg2.extensions import AsIs


class Tars:

    def __init__(self, db=None):
        self.db = db

    def run(self, task, url=None):
        # Run in CLI mode (and stop) if `url` argument was passed.
        if url:
            return self.__scrape(url)

        # Find if video was already scraped before.
        # Update currently processed queue job with metadata stored previously,
        # if any. Otherwise proceed with scraping.
        self.db.execute(
            "SELECT id, url FROM %(table)s WHERE hash = %(hash)s LIMIT 1",
            {'table': AsIs(settings.DB_TABLE_STORE), 'hash': task['hash']}
        )
        metadata = len(self.db.fetchall()) > 0 and self.db.fetchall() or None
        if metadata:
            return self.__update(task['hash'], task['requester'], 'ready')
        else:
            self.__scrape(task['url'])

    def __scrape(self, url):
        pass

    def __update(self, hash, requester, status):
        pass
