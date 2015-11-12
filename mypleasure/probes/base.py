# -*- coding: utf-8 -*-
from datetime import datetime
from mypleasure.utils import Logger


class Base:
    '''
    The interface blueprint for probes.

    Args:
        url: The URL where TARS should find the metadata to fetch.
        logconfig: Dictionary where keys/values match Logger's configuration.
            Defaults to None.
    '''

    def __init__(self, url, logconfig=None):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Capture logger config with fallback to default values.
        setlog = lambda list, key: list[key] if list and key in list else 1

        self.log = Logger(
            verbosity=setlog(logconfig, 'verbosity'),
            reporting=setlog(logconfig, 'reporting')
        )

        self.url = url
        self.processed = False
        self.failed = False
        self.metadata = {
            'title': None,
            'original_url': None,
            'embed_url': None,
            'poster': None,
            'duration': None,
            'naughty': None,
            'created_at': now
        }

    def process(self):
        pass

    def fail(self, msg, data=None):
        self.log.error(
            url=self.url,
            msg=msg,
            data=data
        )
        self.failed = True
        return None

    def get_metadata(self):
        if not self.processed:
            self.process()
            self.processed = True
        return self.metadata
