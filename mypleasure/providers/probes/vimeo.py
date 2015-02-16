import requests
import urlparse
import re
from bs4 import BeautifulSoup
from mypleasure.providers.probes.base import BaseProbe


class Vimeo(BaseProbe):
  """A probe class to crawl and scrape Vimeo videos."""

  name = "Vimeo"


  def process(self):
    response = requests.get(self.url)
    markup = BeautifulSoup(response.text, 'lxml')
    video_wrapper = markup.select('.player_container')[0]

    self.id = self.__extract_id(video_wrapper)

    api_call_url = 'https://vimeo.com/api/v2/video/' + self.id + '.json'
    api_data = requests.get(api_call_url).json()[0]

    self.data['title'] = self.__scrape_title(api_data)
    self.data['poster'] = self.__scrape_poster(api_data)
    self.data['method'] = 'iframe'
    self.data['embed_url'] = '//player.vimeo.com/video/' + self.id
    self.data['duration'] = self.__scrape_duration(api_data)

  def  __extract_id(self, data):
    return re.search("data-clip-id=\"(\d+)\"", str(data)).group(1)


  def __scrape_title(self, data):
    return data['title']


  def __scrape_poster(self, data):
    return data['thumbnail_large']


  def __scrape_duration(self, data):
    duration = data['duration']
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    duration = "%02d:%02d:%02d" % (h, m, s)
    return duration