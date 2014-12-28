import urllib
import datetime
import requests
import bs4
import datetime
import hashlib
from configparser import ConfigParser
from pymongo import MongoClient
from mypleasure.providers import factory


class Tars:
  """TARS mission is to crawl and scrape website for data.

  When invoking the "send_on_mission" method with a URL as an argument,
  TARS attempts to equip itself with the proper provider and if successful,
  will fetch the video.

  Providers are a system of classes ("probes") generated by a factory,
  that will create the fitting apparatus to scrape a website based on its name.

  """


  def __init__(self, debug=False):
    self.url = None
    self.provider = None
    self.markups = []
    self.debug = debug

    config = ConfigParser()
    config.read('settings/settings.cfg')
    host = config.get('mongo', 'host')
    port = config.getint('mongo', 'port')
    db = config.get('mongo', 'db')
    collection = config.get('mongo', 'collection')

    self.mongo = {}
    self.mongo['client'] = MongoClient(host, port)
    self.mongo['db'] = self.mongo['client'][db]
    self.mongo['collection'] = self.mongo['db'][collection]

    self.__log("\n*")
    self.__log("*  TARS, is ready [" + str(datetime.datetime.now()) + "]")
    self.__log("*  ///////////////////////////////////////////")


  def send_on_mission(self, url):
    """Send TARS on a mission to fetch data from video found on the URL passed as argument.

    TARS will retrieve an object representing a video scraped and stored in database.
    The hash for each document in the DB is based on the sanitized URL. It serves as an index key
    to check for existant documents and avoid duplicates. When sent on mission, TARS will first see
    if the hash exists in any DB entries. If so, it'll return the matching entry. Otherwise it will
    proceed with scraping and creating a new entry.

    Args:
      url: The URL where TARS should find the video.

    Returns:
      Either dictionary containing the following attributes related to the video:
      hash, title, poster, method, original_url, embed_url, duration.
      Or None if the provider does not exist for this video.

    """

    mongo_collection = self.mongo['collection']

    url = self.__sanitize_url(url)

    self.__log("*")
    self.__log("*  Creating hash:")
    hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
    self.__log("*    " + hash)

    stored_video = mongo_collection.find_one({ 'hash': hash })

    if stored_video is not None:
      self.__log("*")
      self.__log("*  Found document matching hash in database. Returning:")
      self.__log("*    - hash: " + hash)
      self.__log("*    - title: " + stored_video['title'])
      self.__log("*    - poster: " + stored_video['poster'])
      self.__log("*    - method: " + stored_video['method'])
      self.__log("*    - original url: " + stored_video['original_url'])
      self.__log("*    - embed url: " + stored_video['embed_url'])
      self.__log("*    - duration: " + stored_video['duration'])
      self.__log("*")
      self.__log("*  Done.")
      self.__log("*")
      return stored_video
    else:
      self.scrape(url, hash)


  def scrape(self, url, hash):
    """Scrape the URL and create a new entry indexed with the hash passed as argument.

    Args:
      url: A sanitized URL to scrape.
      hash: A SHA256 hash based on the sanitize URL - serves as index for the document.

    Returns:
      Either dictionary containing the following attributes related to the video:
      hash, title, poster, method, original_url, embed_url, duration.
      Or None if the provider does not exist for this video.

    """

    self.url = url
    self.provider = self.__set_provider(self.url)

    if self.provider is None:
      self.__log("*    - no probe found: aborting mission.")
      self.__log("*\n")
      return None
    else:
      self.__log("*    - found matching probe: " + self.provider.name)
      self.__log("*")

      self.__log("*  Creating payload:")
      self.__log("*    - hash: " + hash)

      title = self.__get_title()
      self.__log("*    - title: " + title)

      poster = self.__get_poster()
      self.__log("*    - poster: " + poster)

      method = self.__get_method()
      self.__log("*    - method: " + method)

      original_url = self.__get_original_url()
      self.__log("*    - original url: " + original_url)

      embed_url = self.__get_embed_url()
      self.__log("*    - embed url: " + embed_url)

      duration = self.__get_duration()
      self.__log("*    - duration: " + duration)
      self.__log("*")

      self.__log("*  Done.")
      self.__log("*")

      video = {}
      video['hash'] = hash
      video['title'] = title
      video['poster'] = poster
      video['method'] = method
      video['original_url'] = original_url
      video['embed_url'] = embed_url
      video['duration'] = duration

      self.__store(video)

      return video


  def __set_provider(self, url):
    """Attempt determining the provider based on the given URL.

    Args:
      url: The URL to scrape.

    Returns:
      A provider probe class if a matching one is found, otherwise None.

    """

    u = urllib.parse.urlsplit(self.url)
    netloc = u.netloc

    if netloc[0:4] == 'www.':
      netloc = netloc[4:]
    netloc = netloc[:netloc.rfind('.')]

    self.__log("*")
    self.__log("*  Determining Provider (fetching probe \"" + netloc + "\"):")

    provider = factory.create(netloc, url)
    return provider


  def __sanitize_url(self, url):
    """Sanitize URL by removing extra arguments."""

    self.__log("*")
    self.__log("*  Sanitizing URL:")
    self.__log("*    - was " + url)

    url = url[:url.rfind('?')]

    self.__log("*    - now " + url)
    return url


  def __store(self, video):
    video['created_at'] = datetime.datetime.utcnow()
    collection = self.mongo['collection']

    if collection.find_one({ 'hash': video['hash'] }) is None:
      self.mongo['collection'].insert(video)


  def __get_title(self):
    """Get 'title' by invoking related method from current provider's probe."""
    return self.provider.get_title()


  def __get_poster(self):
    """Get 'poster' by invoking related method from current provider's probe."""
    return self.provider.get_poster()


  def __get_method(self):
    """Get 'method' by invoking related method from current provider's probe."""
    return self.provider.get_method()


  def __get_original_url(self):
    """Get 'original_url' by invoking related method from current provider's probe."""
    return self.provider.get_original_url()


  def __get_embed_url(self):
    """Get 'embed_url' by invoking related method from current provider's probe."""
    return self.provider.get_embed_url()


  def __get_duration(self):
    """Get 'duration' by invoking related method from current provider's probe."""
    return self.provider.get_duration()


  def __log(self, msg):
    if self.debug is True:
      print(msg)
