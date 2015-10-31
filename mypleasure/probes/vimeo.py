# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from mypleasure.probes.base import Base


class Vimeo(Base):

    def process(self):
        self.log.trace('Launching Vimeo probe.')
        id = self.__get_id(self.__get_page_markup(self.url))
        data = self.__get_data_from_api(self.__get_api_url(id))
        if data:
            return self.__parse_data(data, id)
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

    def __get_api_url(self, id):
        return (
            'https://vimeo.com/api/v2/video/' +
            id + '.json'
        )

    def __get_data_from_api(self, url):
        try:
            return requests.get(url).json()[0]
        except:
            self.fail(
                'Vimeo API\nURL: ' + url + '\n' +
                'Something went wrong while getting ' +
                'data from the API.'
            )
            return None

    def __parse_data(self, json, id):
        self.metadata['title'] = json['title']
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = '//player.vimeo.com/video/' + id
        self.metadata['poster'] = json['thumbnail_large']
        self.metadata['duration'] = self.__get_duration(json['duration'])
        self.metadata['naughty'] = False
        return self.metadata

    def __get_duration(self, input):
        minutes, seconds = divmod(input, 60)
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
