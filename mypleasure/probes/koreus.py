# -*- coding: utf-8 -*-
import re
import time
import requests
from selenium import webdriver
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
        self.metadata['duration'] = self.__get_duration()
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
            meta = markup.select('link[rel="image_src"]')[0]
            return meta['href']
        except Exception, e:
            self.fail(
                'Request on Koreus URL:' + self.url + '\n' +
                'Something went wrong when parsing poster...',
                data=e
            )
            return None

    def __get_duration(self):
        try:
            # Load page in browser. Simulate user clicking
            # on player to start the movie and display duration.
            driver = webdriver.Firefox()
            driver.get(self.url)
            player = driver.find_element_by_id('videoDiv')
            player.click()
            time.sleep(3)
            markup = BeautifulSoup(driver.page_source, 'lxml')
            elm = markup.select('.jw-text-duration')[0].string

            # Format duration.
            if len(elm) == 5:
                duration = '00:' + elm
            return duration
        except Exception, e:
            self.fail(
                'Request on Koreus URL:' + self.url + '\n' +
                'Something went wrong when getting duration...',
                data=e
            )
        finally:
            driver.quit()
