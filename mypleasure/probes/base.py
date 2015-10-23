# -*- coding: utf-8 -*-
from mypleasure.utils import Logger


class Base:
    """
    The interface blueprint for probes.

    Args:
        url: The URL where TARS should find the metadata to fetch.
    """

    def __init__(self, url):
        self.log = Logger()
        self.url = url
        self.error = None
        self.metadata = {
            'title': None,
            'original_url': None,
            'embed_url': None,
            'poster': None,
            'duration': None,
            'naughty': None,
            'created_at': None
        },
        self.process()

    def process(self):
        pass

    def get_metadata(self):
        return self.metadata
