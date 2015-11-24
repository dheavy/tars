# -*- coding: utf-8 -*-
import re
import requests
from mypleasure import settings
from mypleasure.probes.base import Base


class Fb(Base):

    def process(self):
        self.log.trace('Launching Facebook probe.')
        id = self.__get_id(self.url)
        data = self.__get_data_from_api(id, settings.FB_ACCESS_TOKEN)
        if data:
            return self.__parse_data(data, id)
        else:
            self.failed = True
            return None

    def __get_id(self, url):
        matches = re.search("videos/(\d+)", url)
        if matches:
            return matches.group(1)
        return None

    def __get_data_from_api(self, id, access_token):
        try:
            req_uri = 'https://graph.facebook.com/v2.5/%s' \
                '?access_token=%s' \
                '&fields=permalink_url,embed_html,' \
                'title,embeddable,thumbnails,length' % (
                    id, access_token
                )
            res = requests.get(req_uri).json()
        except Exception, e:
            self.fail(
                'Request on Facebook URL: ' + self.url + '\n' +
                'Something went wrong when requesting URL...',
                data=e
            )
            res = None
        return res

    def __parse_data(self, json, id):
        try:
            self.metadata['title'] = json['title']
            self.metadata['original_url'] = self.url
            self.metadata['embed_url'] = self.__get_embed_url(
                json['embed_html']
            )
            self.metadata['poster'] = self.__get_poster(json['thumbnails'])
            self.metadata['duration'] = self.__get_duration(json['length'])
            self.metadata['naughty'] = False
        except Exception, e:
            self.metadata = None
            self.fail(
                'Request on Facebook URL: ' + self.url + '\n' +
                'Something went wrong when parsing API data...',
                data=e
            )
        finally:
            return self.metadata

    def __get_embed_url(self, html):
        try:
            return re.search('src=\"([^"]*)\"', html).group(1)
        except Exception, e:
            self.fail(
                'Request on Facebook URL: ' + self.url + '\n' +
                'Something went wrong when getting embed url...',
                data=e
            )
            return None

    def __get_poster(self, thumbnails):
        try:
            if 'data' in thumbnails:
                data = thumbnails['data']
                tn = data[0]['uri']
                if isinstance(data, list):
                    # Instance with is_preferred==True should
                    # match the most suitable/biggest image.
                    tn = [x for x in data if x['is_preferred'] is True]
                    if len(tn) > 0 and 'uri' in tn[0]:
                        tn = tn[0]['uri']
        except Exception, e:
            tn = ''
            self.fail(
                'Request on Facebook URL: ' + self.url + '\n' +
                'Something went wrong when getting poster data...',
                data=e
            )
        finally:
            return tn

    def __get_duration(self, input):
        minutes, seconds = divmod(input, 60)
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
