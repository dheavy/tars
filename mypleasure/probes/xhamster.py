# -*- coding: utf-8 -*-
# http://xhamster.com/movies/4476488/
# hotgold_two_slutty_czech_babes_love_taking_it_up_the_ass.html
# ?from=video_promo
import re
import requests
from bs4 import BeautifulSoup
from mypleasure.probes.base import Base


class Xhamster(Base):

    def process(self):
        self.log.trace('Launching XHamster probe.')
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
                'Request on Xhamster URL:' + url + '\n' +
                'Something went wrong when requesting URL....'
            )
        finally:
            return res

    def __get_id(self, url):
        return re.search("movies/(\d+)/", url).group(1)

    def __parse_data(self, markup, id):
        self.metadata['title'] = markup.select(
            '#playerBox h1'
        )[0].string.strip()
        self.metadata['original_url'] = self.__get_original_url(self.url)
        self.metadata['embed_url'] = '//xhamster.com/xembed.php?video=' + id
        self.metadata['poster'] = self.__get_poster(markup)
        self.metadata['duration'] = self.__get_duration(markup)
        self.metadata['naughty'] = True
        markup.decompose()
        return self.metadata

    def __get_original_url(self, url):
        if '?' in url:
            url = url[:url.rfind('?')]
        return url

    def __get_poster(self, markup):
        try:
            player_settings = re.search(
                "(vars:\s{.*\"}})", str(markup)
            ).group(1)
            image = re.search(
                "\"image\":\"http:([^\"]*)", player_settings
            ).group(1)
            poster = image.replace('\/', '/')
        except Exception, e:
            poster = ''
            self.fail(
                'Request on XHamster URL: ' + self.url + '\n' +
                'Something went wrong when getting poster...',
                data=e
            )
        finally:
            return poster

    def __get_duration(self, markup):
        tag = str(markup.select('#videoUser div.item')[1])
        duration = tag[tag.rfind('/span>') + 6:-6].strip()

        # Format duration to `hh:mm:ss`.
        # -------------------------------
        # Xhamster neglects formating hours.
        # So if a movie lasts more than an hour,
        # it will still be displayed as `mm:ss`,
        # or even `mmm:ss` if needed - e.g. a movie
        # lasting 01:10:20 will be displayed as
        # 70:20 on Xhamster.

        first_digits = int(duration[:2])
        last_digits = str(duration[-2:])

        # If movie lasts less than an hour, add trailing 0s.
        if first_digits < 60:
            duration = '00:' + duration

        # If movie lasts more than an hour, convert and ajdust.
        else:
            h = str(first_digits // 60)
            mn = str(first_digits % 60)

            if len(h) < 2:
                h = '0' + h
            if len(mn) < 2:
                mn = '0' + mn

            duration = h + ':' + mn + ':' + last_digits

        return duration
