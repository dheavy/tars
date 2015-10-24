# -*- coding: utf-8 -*-


import requests
import urlparse
from mypleasure.probes.base import Base


class Youtube(Base):

    def process(self):
        self.log.trace('Launching Youtube probe.')
        id = self.__get_id(self.url)
        data = self.__get_data_from_api(self.__get_api_url(id))
        d = self.__parse_data(data, id)
        print(d)

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
        res = requests.get(url)
        json = res.json()
        if 'error' in json:
            self.fail(
                'Youtube API call\nURL: %(url)s \nError: %(err)s'
                % {'url': url, 'err': json['error']}
            )
        else:
            return json

    def __get_api_url(self, id):
        return (
            "https://noembed.com/embed?url=" +
            "https://www.youtube.com/watch?v=%(id)s"
            % {'id': id}
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
        pass
        # minutes, seconds = divmod(json)
        # hours, minutes = divmod(minutes, 60)
        # return "%02d:%02d:%02d" % (hours, minutes, seconds)
