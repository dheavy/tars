import requests
import re
from bs4 import BeautifulSoup
from mypleasure.providers.probes.base import BaseProbe


class Youporn(BaseProbe):

  name = "Youporn"

  def process(self):
    response = requests.get(self.url)
    markup = BeautifulSoup(response.text, 'lxml')

    self.data['id'] = self.__extract_id()
    self.data['title'] = self.__scrape_title(markup)
    self.data['poster'] = self.__scrape_poster(markup)
    self.data['method'] = 'iframe'
    self.data['embed_url'] = 'http://www.youporn.com/embed/' + self.data['id']
    self.data['duration'] = self.__scrape_duration()

    markup.decompose()

  def __extract_id(self):
    return re.search("watch/(\d+)/", self.url).group(1)

  def __scrape_title(self, markup):
    return markup.select('#watchHeader h1')[0].string

  def __scrape_poster(self, markup):
    return markup.select('#player-html5')[0]['poster']

  def __scrape_duration(self):
    response = requests.get('http://www.youporn.com/search/?query=' + self.data['title'])

    markup = BeautifulSoup(response.text, 'lxml')
    duration = markup.select('.videoList .duration')[0].string
    markup.decompose()

    return duration
