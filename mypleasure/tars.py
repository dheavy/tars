# -*- coding: utf-8 -*-


import sys
import urlparse
from psycopg2.extensions import AsIs
from . import settings
from .probes import factory as probe_factory


class Tars:
    """
    TARS fetches metadata and returns it upon invocation
    of the run() method.

    Invoking run() method with a URL as argument,
    TARS Attempts to equip itself with the adequate "probe",
    i.e. a class dealing with fetching data through APIs or
    scraping, depending of the service we want to access.

    Probes are classes implementing the same interface and
    generated by a factory.

    """

    def __init__(self, db=None):
        self.db = db

    def run(self, job, url=None):
        # Run in CLI mode (and stop) if `url` argument was passed.
        if url:
            return self.__scrape(url)
            sys.exit()

        # Find if video was already scraped before.
        # Update currently processed queue job with metadata stored previously,
        # if any. Otherwise proceed with scraping.
        self.db.execute(
            "SELECT id, url FROM %(table)s WHERE hash = %(hash)s LIMIT 1",
            {'table': AsIs(settings.DB_TABLE_QUEUE), 'hash': job['hash']}
        )
        metadata = len(self.db.fetchall()) > 0 and self.db.fetchall() or None
        if metadata:
            return self.__update_queue(
                job['hash'], job['requester'], 'ready'
            )
        else:
            self.__scrape(job['url'])

    def __scrape(self, url):
        self.__probe_from_url(url)
        pass

    def __update_queue(self, hash, requester, status):
        pass

    def __probe_from_url(self, url):
        # Extract service name from URL.
        netloc = urlparse.urlsplit(url).netloc
        if netloc[0:4] == 'www.':
            netloc = netloc[4:]
        netloc = netloc[:netloc.rfind('.')]

        # Invoke factory method to instantiate a matchin probe.
        return probe_factory.create(netloc, url)
