# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from mypleasure.probes.base import Base


class Youporn(Base):

    def process(self):
        self.log.trace('Lauching Youporn probe.')
        markup = self.__get_page_markup(self.url)
        try:
            id = self.__get_id(self.url)
            data = self.__parse_data(markup, id)
            return data
        except:
            self.failed = True
            return None

    def __get_page_markup(self, url):
        try:
            res = requests.get(url)
            res = BeautifulSoup(res.text, 'lxml')
        except:
            res = None
            self.fail(
                'Request on Youporn URL:' + url + '\n' +
                'Something went wrong when requesting URL....'
            )
        return res

    def __get_id(self, url):
        return re.search("watch/(\d+)/", url).group(1)

    def __parse_data(self, markup, id):
        self.metadata['title'] = markup.select('#watchHeader h1')[0].string
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = '//www.youporn.com/embed/' + id
        self.metadata['poster'] = markup.select('#player-html5')[0]['poster']
        self.metadata['duration'] = self.__get_duration(
            self.url, self.metadata['title']
        )
        self.metadata['naughty'] = True
        return self.metadata

    def __get_duration(self, url, title):
        try:
            # Get duration displayed from search results.
            res = requests.get(
                'http://www.youporn.com/search/?query=' + title
            )
            markup = BeautifulSoup(res.text, 'lxml')
            duration = markup.select('.videoList .duration')[0].string

            # Format hours display (two digits).
            if len(duration) < 6:
                duration = '00:' + duration

            if len(duration) < 8:
                duration = '0' + duration

            markup.decompose()
        except:
            duration = '--:--:--'
        finally:
            return duration
