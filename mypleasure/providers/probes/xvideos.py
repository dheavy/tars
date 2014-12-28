import requests
import re
from bs4 import BeautifulSoup
from mypleasure.providers.probes.base import BaseProbe


class Xvideos(BaseProbe):
  """A probe class to crawl and scrape on Xvideos.com."""

  name = "Xvideos"


  def process(self):
    response = requests.get(self.url)
    markup = BeautifulSoup(response.text, 'lxml')

    id = self.__extract_id()
    self.data['title'] = self.__scrape_title(markup)
    self.data['poster'] = self.__scrape_poster(markup)
    self.data['method'] = 'iframe'
    self.data['embed_url'] = 'http://flashservice.xvideos.com/embedframe/' + id
    self.data['duration'] = self.__scrape_duration(markup)

    markup.decompose()

  def __extract_id(self):
    return re.search("/video(\d+)/", self.url).group(1)


  def __scrape_title(self, markup):
    raw = str(markup.select('#page #main h2')[0])
    title = raw[4:raw.find('span')-1].strip()
    return title


  def __scrape_poster(self, markup):
    meta = str(markup.select('#flash-player-embed')[0])
    return re.search("url_bigthumb=(.+)&amp;key", meta).group(1)


  def __scrape_duration(self, markup):
    raw = markup.select('#main .duration')[0].string
    raw = raw[2:].strip()

    # Duration is formatted as such: hh:mm:ss
    duration = ''

    # Movie lasts more than an hour...
    if 'h' in raw:
      h = raw[:raw.rfind('h')].strip()
      duration += '0' + h + ':'

      # ...with some defined minutes maybe? Else fall back.
      if 'min' in raw:
        mn = raw[raw.find(' '):raw.rfind('min')].strip()
        if len(mn) < 2:
          mn = '0' + mn
      else:
        mn = '00'

      duration += mn

      # I could find any video display hh:mm and ss on the site.
      # It does not mean it doesn't or will never exist, but for
      # now, this will do.
      duration += ':00'

    # Movie lasts more than a minute...
    if 'h' not in raw and 'min' in raw:
      duration = '00:'

      mn = raw[:raw.rfind('min')].strip()

      if len(mn) < 2:
        mn = '0' + mn

      duration += mn

      # ...with defined seconds, else fall back.
      if 'sec' in raw:
        sec = raw[raw.index('min')+3:raw.rfind('sec')].strip()
        if len(sec) < 2:
          sec = '0' + sec
      else:
        sec = '00'

      duration += ':' + sec

    # Movie lasts only seconds.
    if 'h' not in raw and 'min' not in raw and 'sec' in raw:
      duration = '00:00:'

      sec = re.search('(\d+)', raw).group(1)
      if len(sec) < 2:
        sec = '0' + sec

      duration += sec

    return duration
