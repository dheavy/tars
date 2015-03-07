import requests, re, sys
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from mypleasure.scrapers.probes.base import BaseProbe


class Youporn(BaseProbe):
  """A probe class to crawl and scrape Youporn videos."""

  name = "Youporn"
  nsfw = True


  def process(self):
    try:
      response = requests.get(self.url)
    except ConnectionError:
      print('Could not connect to address: ' + self.url)
      sys.exit()

    markup = BeautifulSoup(response.text, 'lxml')

    id = self.__extract_id()
    self.data['title'] = self.__scrape_title(markup)
    self.data['poster'] = self.__scrape_poster(markup)
    self.data['method'] = 'iframe'
    self.data['embed_url'] = '//www.youporn.com/embed/' + id
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

    # Format hours display (two digits)
    if len(duration) < 6:
      duration = '00:' + duration

    if len(duration) < 8:
      duration = '0' + duration

    markup.decompose()

    return duration
