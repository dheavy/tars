# -*- coding: utf-8 -*-


import requests
import urlparse
from mypleasure.probes.base import Base


class Dailymotion(Base):

    def process(self):
        self.log.trace('Launching Dailymotion probe.')
        id = self.__get_id(self.url)
        data = self.__get_data_from_api(self.__get_api_url(id))
        if data and 'error' not in data:
            return self.__parse_data(data, id)
        else:
            self.failed = True
            return None

    def __get_id(self, url):
        return (urlparse.urlparse(url).path[7:])[0:]

    def __get_data_from_api(self, url):
        try:
            return requests.get(url).json()
        except:
            self.fail(
                'Dailymotion API\nURL: ' + url + '\n' +
                'Something went wrong when calling API ' +
                'when processing results...'
            )

    def __get_api_url(self, id):
        return (
            "https://api.dailymotion.com/video/" +
            id + "?fields=duration,embed_url," +
            "thumbnail_720_url,title,url"
        )

    def __parse_data(self, json, id):
        self.metadata['title'] = json['title']
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = self.__get_embed_url(id)
        self.metadata['poster'] = json['thumbnail_720_url']
        self.metadata['duration'] = self.__get_duration(json)
        self.metadata['naughty'] = False
        return self.metadata

    def __get_embed_url(self, id):
        return '//www.dailymotion.com/embed/video/'.format(id)

    def __get_duration(self, json):
        minutes, seconds = divmod(json['duration'], 60)
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
