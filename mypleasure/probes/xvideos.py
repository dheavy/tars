# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from mypleasure.probes.base import Base


class Xvideos(Base):

    def process(self):
        self.log.trace('Launching XVideos probe.')
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
                'Request on Xvideos URL:' + url + '\n' +
                'Something went wrong when requesting URL....'
            )
        finally:
            return res

    def __get_id(self, url):
        return re.search("/video(\d+)/", self.url).group(1)

    def __parse_data(self, markup, id):
        self.metadata['title'] = self.__get_title(markup)
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = (
            '//flashservice.xvideos.com/embedframe/' + id
        )
        self.metadata['poster'] = self.__get_poster(markup)
        self.metadata['duration'] = self.__get_duration(markup)
        self.metadata['naughty'] = True
        return self.metadata

    def __get_title(self, markup):
        raw = str(markup.select('#page #main h2')[0])
        return raw[4:raw.find('span') - 1].strip()

    def __get_poster(self, markup):
        meta = str(markup.select('#flash-player-embed')[0])
        return re.search("url_bigthumb=(.+)&amp;key", meta).group(1)

    def __get_duration(self, markup):
        raw = markup.select('#main .duration')[0].string
        raw = raw[2:].strip()

        # Duration is formatted as such: hh:mm:ss
        duration = ''

        # Movie lasts more than an hour...
        if 'h' in raw:
            hours = raw[:raw.rfind('h')].strip()
            duration += '0' + hours + ':'

            # ...with minutes defined maybe?
            # Otherwise just fall back.
            if 'min' in raw:
                minutes = raw[raw.find(' '):raw.rfind('min')].strip()
                if len(minutes) < 2:
                    minutes = '0' + minutes
            else:
                minutes = '00'
            duration += minutes

            # I couldn't find any video displaying "hh:mn" and "ss"
            # on the site. It doesn't mean there's none or never will be,
            # but for now, the following will do.
            duration += ':00'

        # Movie lasts less than an hour but more than a minute...
        if 'h' not in raw and 'min' in raw:
            duration = '00:'
            minutes = raw[:raw.rfind('min')].strip()
            if len(minutes) < 2:
                minutes = '0' + minutes
            duration += minutes

            # Add defined seconds, or else fall back.
            if 'sec' in raw:
                seconds = raw[raw.index('min') + 3:raw.rfind('sec')].strip()
                if len(seconds) < 2:
                    seconds = '0' + seconds
            else:
                seconds = '00'
            duration += ':' + seconds

        # Movie lasts less than a minute...
        if 'h' not in raw and 'min' not in raw and 'sec' in raw:
            duration += '00:00:'
            seconds = re.search('(\d+)', raw).group(1)
            if len(seconds) < 2:
                seconds = '0' + seconds
            duration += seconds

        return duration
