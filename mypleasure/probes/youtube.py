# -*- coding: utf-8 -*-
import isodate
import requests
import urlparse

from mypleasure import settings
from mypleasure.probes.base import Base


class Youtube(Base):

    def process(self):
        self.log.trace('\nLaunching Youtube probe.')
        id = self.__get_id(self.url)
        data, api_used = self.__get_data_from_api(id)
        if data:
            metadata = self.__parse_data(data, id, api_used)
        else:
            self.failed = True
            metadata = None
        return metadata

    def __get_id(self, url):
        parsed = urlparse.urlparse(url)
        query = urlparse.parse_qs(parsed.query)
        getvar = ('v' in query and len(query['v']) > 0) and query['v'][0] or ''
        if getvar and '?' in getvar:
            result = getvar[:getvar.find('?')]
        else:
            result = getvar
        return result

    def __get_data_from_api(self, id):
        api_used = 'youtube'
        json = self.__get_data_from_youtube(
            self.__get_api_url(id, service='youtube')
        )
        if json is None:
            json = self.__get_data_from_noembed(
                self.__get_api_url(id)
            )
            api_used = 'noembed'
        return json, api_used

    def __get_data_from_youtube(self, url):
        try:
            res = requests.get(url)
            try:
                json = res.json()
                if 'items' in json:
                    if len(json['items']) == 0:
                        self.fail(
                            'Youtube API\nURL: ' + url + '\n' +
                            'Result payload is empty...'
                        )
                        return None
                    else:
                        return json['items'][0]
            except:
                self.fail(
                    'Youtube API\nURL: ' + url + '\n' +
                    'Failed to fetch JSON data from API'
                )
                return None
        except:
            self.fail('Could not connect to address ' + url)
            return None

    def __get_data_from_noembed(self, url):
        try:
            res = requests.get(url)
            json = res.json()
            if 'error' in json:
                self.fail(
                    'Noembed (Youtube)\nURL: %(url)s \nError: %(err)s'
                    % {'url': url, 'err': json['error']}
                )
                return None
            else:
                return json
        except:
            self.fail('Could not connect to address ' + url)
            return None

    def __get_api_url(self, id, service=None):
        if service == 'youtube':
            key = settings.YOUTUBE_API_KEY
            if key:
                return (
                    "https://www.googleapis.com/youtube/v3/videos" +
                    "?part=snippet%2CcontentDetails&id=" + id +
                    "&fields=items(contentDetails%2Csnippet%2Cid)&key=" +
                    key
                )
            else:
                return None
        else:
            return (
                "https://noembed.com/embed?url=" +
                "https://www.youtube.com/watch?v=%(id)s"
                % {'id': id}
            )

    def __parse_data(self, json, id, api_used):
        self.metadata['title'] = self.__get_title(api_used, json)
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = self.__get_embed_url(id)
        self.metadata['poster'] = self.__get_poster(id, api_used, json=json)
        self.metadata['duration'] = self.__get_duration(api_used, json=json)
        self.metadata['naughty'] = False
        return self.metadata

    def __get_title(self, api_used, json):
        if api_used == 'youtube':
            return json['snippet']['title']
        else:
            return json['title']

    def __get_embed_url(self, id):
        return "//www.youtube.com/embed/{0}".format(id)

    def __get_poster(self, id, api_used, json=False):
        tn = '//img.youtube.com/vi/%s/mqdefault.jpg'.format(id)
        if api_used == 'youtube' and json:
            try:
                return json['snippet']['thumbnails']['default']['url']
            except:
                pass
        else:
            return '//img.youtube.com/vi/%s/mqdefault.jpg'.format(id)
        return tn

    def __get_duration(self, api_used, json=False):
        if api_used == 'youtube' and json:
            try:
                duration = json['contentDetails']['duration']
                seconds = isodate.parse_duration(duration).total_seconds()
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                return "%02d:%02d:%02d" % (hours, minutes, seconds)
            except:
                # Log an error, but carry on.
                self.log.error(
                    url=self.url,
                    msg="Youtube API call - failed to get duration"
                )
        return '--:--:--'
