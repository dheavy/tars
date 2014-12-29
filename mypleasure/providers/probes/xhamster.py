import requests
import re
from bs4 import BeautifulSoup
from mypleasure.providers.probes.base import BaseProbe


class Xhamster(BaseProbe):
  """A probe to crawl and scrape on xhamster.com"""

  name = "Xhamster"


  def process(self):
    response = requests.get(self.url)
    markup = BeautifulSoup(response.text, 'lxml')

    id = self.__extract_id()
    self.data['title'] = self.__scrape_title(markup)
    self.data['poster'] = self.__scrape_poster(markup)
    self.data['method'] = 'iframe'
    self.data['embed_url'] = 'http://xhamster.com/xembed.php?video=' + id
    self.data['duration'] = self.__scrape_duration(markup)

    markup.decompose()


  def __extract_id(self):
    return re.search("movies/(\d+)/", self.url).group(1)


  def __scrape_title(self, markup):
    return markup.select('#playerBox h1')[0].string.strip()


  def __scrape_poster(self, markup):
    tag = markup.select('#player video')[0]
    return tag['poster']


  def __scrape_duration(self, markup):
    tag = str(markup.select('#videoUser div.item')[1])
    duration = tag[tag.rfind('/span>')+6:-6].strip()

    # Format duration to `hh:mm:ss`.
    # -------------------------------
    # Xhamster neglects formating hours. So if a movie lasts more than an hour,
    # it will still be displayed as `mm:ss`, or even `mmm:ss` if needed
    # - e.g. a movie lasting 01:10:20 will be displayed as 70:20 on Xhamster.

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
