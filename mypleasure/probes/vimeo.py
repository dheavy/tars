# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from mypleasure.probes.base import Base


class Vimeo(Base):

    def process(self):
        self.log.trace('Launching Vimeo probe.')
        id = self.__get_id(self.__get_page_markup(self.url))
        data, api_used = self.__get_data_from_api(id)
        if data:
            return self.__parse_data(data, id, api_used)
        else:
            self.failed = True
            return None

    def __get_page_markup(self, url):
        try:
            res = requests.get(url)
            res = BeautifulSoup(res.text, 'lxml')
        except:
            res = None
            self.fail(
                'Request on Vimeo URL:' + url + '\n' +
                'Something went wrong when requesting URL....'
            )
        finally:
            return res

    def __get_id(self, markup):
        if markup:
            try:
                player_container = markup.select('.player_container')
                return re.search(
                    "data-clip-id=\"(\d+)\"",
                    str(player_container[0])
                ).group(1)
            except:
                self.fail(
                    'Failed to extract Vimeo ID from markup.',
                    data=player_container
                )
                return None
            finally:
                markup.decompose()
        return None

    def __get_api_url(self, id, service):
        if service is 'VimeoAPIv2':
            return (
                'https://vimeo.com/api/v2/video/' +
                str(id) + '.json'
            )
        if service is 'noembed':
            return (
                "https://noembed.com/embed?url=" +
                "https://www.vimeo.com/%(id)s"
                % {'id': id}
            )

    def __get_data_from_api(self, id):
        api_used = 'VimeoAPIv2'
        json = self.__get_data_from_api_v2(
            self.__get_api_url(id, service='VimeoAPIv2')
        )
        if json is None:
            json = self.__get_data_from_noembed(
                self.__get_api_url(id, service='noembed')
            )
            api_used = 'noembed'
        return json, api_used

    def __get_data_from_api_v2(self, url):
        try:
            return requests.get(url).json()[0]
        except:
            self.fail(
                'Vimeo API v2\nURL: ' + url + '\n' +
                'Something went wrong while getting ' +
                'data from the API.'
            )
            return None

    def __get_data_from_noembed(self, url):
        try:
            res = requests.get(url)
            json = res.json()
            if 'error' in json:
                self.fail(
                    'Noembed (Vimeo)\nURL: %(url)s \nError: %(err)s'
                    % {'url': url, 'err': json['error']}
                )
                return None
            else:
                return json
        except:
            self.fail('Could not connect to address ' + url)
            return None

    def __parse_data(self, json, id, api_used):
        self.metadata['title'] = json['title']
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = '//player.vimeo.com/video/' + id
        self.metadata['poster'] = self.__get_poster(id, api_used, json)
        self.metadata['duration'] = self.__get_duration(json['duration'])
        self.metadata['naughty'] = False
        return self.metadata

    def __get_poster(self, id, api_used, json=False):
        if api_used == 'VimeoAPIv2' and json:
            return json['thumbnail_large']
        elif api_used == 'noembed' and json:
            return json['thumbnail_url']
        return ''

    def __get_duration(self, input):
        minutes, seconds = divmod(input, 60)
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
