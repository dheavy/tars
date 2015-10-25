# -*- coding: utf-8 -*-
from datetime import datetime
from mypleasure.utils import Logger


class Base:
    """
    The interface blueprint for probes.

    Args:
        url: The URL where TARS should find the metadata to fetch.
    """

    def __init__(self, url):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log = Logger()
        self.url = url
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
        self.process()

    def process(self):
        pass

    def fail(self, msg, data=None):
        self.log.error(
            url=self.url,
            msg=msg,
            data=data
        )
        self.failed = True

    def get_metadata(self):
        return self.metadata
