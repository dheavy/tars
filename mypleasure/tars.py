# -*- coding: utf-8 -*-
import sys
import urlparse
from psycopg2.extensions import AsIs
from . import settings
from .probes import factory as probe_factory


class Tars:
    '''
    TARS fetches metadata and returns it upon invocation
    of the run() method.

    Invoking run() method with a URL as argument,
    TARS Attempts to equip itself with the adequate "probe",
    i.e. a class dealing with fetching data through APIs or
    scraping, depending of the service we want to access.

    Probes are classes implementing the same interface and
    generated by a factory.

    Args:
        db: A psycopg2 database cursor for transactions, if TARS is expected
            to update the media queue. Defaults to None.
    '''

    def __init__(self, db=None):
        self.db = db

    def run(self, job, url=None, verbosity=1, reporting=0):
        '''
        Runs a fetching job. Delegates to relevant probe based on given URL.

        Args:
            job: Dictionary of job fetched from media processing queue.
                If set, runs the aformentioned job and mutate status in queue
                upon success or failure.
            url: String of a URL to fetch. Defaults to None. If set, switches
                TARS to CLI mode, leaving the queue untouched and printing
                result to console if logging verbosity allows it.
            verbosity: Integer describing verbosity level for the Logger.
                Defaults to 1.
            reporting: Integer describing reporting level for the Logger.
                Defaults to 1.

        Returns:
            A dictionary of metadata pertaining to the analysis media/URL,
            or None if nothing relevant is found.
        '''
        self.verbosity = verbosity
        self.reporting = reporting

        # Run in CLI mode (and stop) if `url` argument was passed.
        if url:
            return self.__fetch(url=url)
            sys.exit()

        # Find if video was already scraped before.
        # Update currently processed queue job with metadata stored previously,
        # if any. Otherwise proceed with scraping.
        self.db.execute(
            "SELECT id, origin_url FROM %(t)s WHERE hash = %(h)s LIMIT 1",
            {'t': AsIs(settings.DB_TABLE_STORE), 'h': job['hash']}
        )
        if len(self.db.fetchall()) > 0 and self.db.fetchall()[0]:
            return self.__update_queue(job['hash'], job['requester'], 'ready')
        else:
            return self.__fetch(job=job)

    def __fetch(self, url=None, job=None):
        if job and 'url' in job:
            probe = self.__probe_from_url(job['url'])
        else:
            probe = self.__probe_from_url(url)

        if probe:
            metadata = probe.get_metadata()

        if probe is None or probe.failed:
            if job and all(k in job for k in ('requester', 'status', 'hash')):
                self.__update_queue(job['hash'], job['requester'], 'failed')
            return None
        else:
            if job and all(k in job for k in ('requester', 'status', 'hash')):
                self.__update_queue(job['hash'], job['requester'], 'ready')
        return metadata

    def __update_queue(self, hash, requester, status):
        self.db.execute(
            "UPDATE %(t)s SET status=%(s)s WHERE \
            requester=%(r)s AND hash=%(h)s",
            {
                't': AsIs(settings.DB_TABLE_QUEUE),
                's': status,
                'h': hash,
                'r': requester
            }
        )

    def __probe_from_url(self, url):
        # Extract service name from URL.
        netloc = urlparse.urlsplit(url).netloc
        if netloc[0:4] == 'www.':
            netloc = netloc[4:]
        netloc = netloc[:netloc.rfind('.')]

        # Invoke factory method to instantiate a matchin probe.
        return probe_factory.create(
            netloc, url,
            logconfig={
                'verbosity': self.verbosity,
                'reporting': self.reporting
            }
        )
