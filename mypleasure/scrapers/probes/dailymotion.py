import requests
import re
import sys
import urlparse
from mypleasure.scrapers.probes.base import BaseProbe


class Dailymotion(BaseProbe):
  """A probe class to crawl and scrape Dailymotion videos."""

  name = "Dailymotion"


  def process(self):
    id = self.__extract_id()
    api_call_url = 'https://api.dailymotion.com/video/' + id + '?fields=duration,embed_url,thumbnail_720_url,title,url'
    api_data = requests.get(api_call_url).json()

    self.data['title'] = api_data['title']
    self.data['poster'] = api_data['thumbnail_720_url']
    self.data['method'] = 'iframe'
    self.data['embed_url'] = '//www.dailymotion.com/embed/video/' + id
    self.data['duration'] = self.__scrape_duration(api_data)


  def __extract_id(self):
    long_id = urlparse.urlparse(self.url).path[7:]
    id = long_id[0:long_id.find('_')]
    return id


  def __scrape_duration(self, data):
    duration = data['duration']
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    duration = "%02d:%02d:%02d" % (h, m, s)
    return duration