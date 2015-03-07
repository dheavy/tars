import requests
import urlparse
from mypleasure.scrapers.probes.base import BaseProbe


class Youtube(BaseProbe):
  """A probe class to crawl and scrape Youtube videos."""

  name = "Youtube"
  nsfw = False


  def process(self):
    try:
      response = requests.get(self.url)
    except ConnectionError:
      print('Could not connect to address: ' + self.url)
      sys.exit()

    self.id = self.__extract_id()
    api_call_url = 'https://gdata.youtube.com/feeds/api/videos/' + self.id + '?v=2&alt=jsonc'
    api_data = requests.get(api_call_url).json()['data']

    self.data['title'] = self.__scrape_title(api_data)
    self.data['poster'] = self.__scrape_poster()
    self.data['method'] = 'iframe'
    self.data['embed_url'] = '//www.youtube.com/embed/' + self.id
    self.data['duration'] = self.__scrape_duration(api_data)


  def __extract_id(self):
    url_data = urlparse.urlparse(self.url)
    query = urlparse.parse_qs(url_data.query)
    return query['v'][0]


  def __scrape_title(self, data):
    return data['title']


  def  __scrape_poster(self):
    return 'http://img.youtube.com/vi/' + self.id + '/mqdefault.jpg'


  def __scrape_duration(self, data):
    duration = data['duration']
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    duration = "%02d:%02d:%02d" % (h, m, s)
    return duration