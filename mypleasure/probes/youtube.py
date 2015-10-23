# -*- coding: utf-8 -*-


import requests
import urlparse
from .base import Base
from mypleasure.utils import Logger


class Youtube(Base):

    def process(self):
        id = self.__get_id(self.url)
        data = self.__get_data_from_api(self.__get_api_url(id))
        return self.__parse_data(data, id)

    def __get_id(self, url):
        parsed = urlparse.urlparse(url)
        query = urlparse.parse_qs(parsed.query)
        getvar = query['v'][0]
        if getvar and '?' in getvar:
            result = getvar[:getvar.find('?')]
        else:
            result = getvar
        return result

    def __get_data_from_api(self, url):
        try:
            json = requests.get(url).json()
            return json['data']
        except:
            log = Logger()
            log.error('Could not connect to Youtube\'s API')

    def __get_api_url(self, id):
        return (
            'https://gdata.youtube.com/feeds/api/videos/ \
            %s?v=2&alt=jsonc'.format(id)
        )

    def __parse_data(self, json, id):
        self.metadata['title'] = json['title']
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = self.__get_embed_url(id)
        self.metadata['poster'] = self.__get_poster(id)
        self.metadata['duration'] = self.__get_duration(json)
        self.metadata['naughty'] = False

    def __get_embed_url(self, id):
        return '//www.youtube.com/embed/%s'.format(id)

    def __get_poster(self, id):
        return '//img.youtube.com/vi/%s/mqdefault.jpg'.format(id)

    def __get_duration(self, json):
        minutes, seconds = divmod(json['data'])
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
