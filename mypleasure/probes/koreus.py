# -*- coding: utf-8 -*-
import re
import requests
import subprocess
from bs4 import BeautifulSoup
from mypleasure.probes.base import Base


class Koreus(Base):

    def process(self):
        self.log.trace('Launching Koreus probe.')
        markup = self.__get_page_markup(self.url)
        try:
            id = self.__get_id(self.url)
            data = self.__parse_data(markup, id)
        except:
            data = None
            self.failed = True
        finally:
            return data

    def __get_id(self, url):
        try:
            id = re.search("/video/(.*)", url).group(1)
            id = id[:id.rfind('.')]
            return id
        except Exception, e:
            self.fail(
                'Request on Koreus URL:' + url + '\n' +
                'Something went wrong when parsing ID...',
                data=e
            )
            return None

    def __get_page_markup(self, url):
        try:
            res = requests.get(url)
            res = BeautifulSoup(res.text, 'lxml')
        except Exception, e:
            res = None
            self.fail(
                'Request on Koreus URL:' + url + '\n' +
                'Something went wrong when requesting URL...',
                data=e
            )
        finally:
            return res

    def __parse_data(self, markup, id):
        self.metadata['title'] = self.__get_title(markup)
        self.metadata['original_url'] = self.url
        self.metadata['embed_url'] = (
            '//www.koreus.com/embed/' + id
        )
        self.metadata['poster'] = self.__get_poster(markup)
        self.metadata['duration'] = self.__get_duration(markup)
        self.metadata['naughty'] = False
        return self.metadata

    def __get_title(self, markup):
        try:
            meta = markup.select('meta[property="og:title"]')[0]
            return meta['content']
        except Exception, e:
            self.fail(
                'Request on Koreus URL:' + self.url + '\n' +
                'Something went wrong when parsing title...',
                data=e
            )
            return None

    def __get_poster(self, markup):
        try:
            meta = markup.select('meta[property="og:image"]')[0]
            return meta['content']
        except Exception, e:
            self.fail(
                'Request on Koreus URL:' + self.url + '\n' +
                'Something went wrong when parsing poster...',
                data=e
            )
            return None

    def __get_duration(self, markup):
        try:
            # Get duration directly from video metadata.
            filename = re.search(
                '(?:file:\s")([^\"].*)(.mp4)', str(markup)
            ).group(1)
            filename += '.mp4'

            video = subprocess.Popen(
                ['ffprobe', filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            duration = [x for x in video.stdout.readlines() if 'Duration' in x]
            duration = duration[0]
            duration = re.search(
                "(?:(?:\[)?(?:\')?(?:\s*)"
                "?Duration:(?:\s*)?)(\d{2}:\d{2}:\d{2})",
                duration
            ).group(1)
        except Exception, e:
            duration = '--:--:--'
            self.fail(
                'Request on Koreus URL:' + self.url + '\n' +
                'Something went wrong when getting duration...',
                data=e
            )
        finally:
            return duration
