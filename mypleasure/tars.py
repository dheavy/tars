# -*- coding: utf-8 -*-

import os
import urlparse
import datetime
import requests
import bs4
import datetime
import hashlib
from ConfigParser import ConfigParser
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

    # Set up variables.
    # If `debug` is True, TARS will output to stdout.
    self.url = None
    self.provider = None
    self.requester = None
    self.debug = debug

    # Set up and read config for DB.
    if os.environ['LARAVEL_ENV'] and os.environ['LARAVEL_ENV'] == 'local':
      config = ConfigParser()
      config.read('settings/settings.cfg')
      db = config.get('mongo', 'db')
      host = config.get('mongo', 'host')
      port = config.getint('mongo', 'port')
      collection = config.get('mongo', 'collection')
      queue = config.get('mongo', 'queue')
    else:
      MONGO_URL = os.environ.get('MONGOHQ_URL')
      host = os.environ['MONGODB_HOST']
      port = int(os.environ['MONGODB_PORT'])
      db = os.environ['MONGODB_DATABASE']
      port = os.environ['MONGODB_PORT']
      collection = 'videos'
      queue = 'queue'

    # Setup MongoDB.
    self.mongo = {}
    host = host + ':' + str(port)
    self.mongo['client'] =  MongoClient(MONGO_URL)
    self.mongo['db'] = self.mongo['client'][db]
    self.mongo['collection'] = self.mongo['db'][collection]
    self.mongo['queue'] = self.mongo['db'][queue]


  def send_on_mission(self, args, forceUrl=None):
    """Send TARS on a mission to fetch data from video found on the URL passed as argument.

    TARS will retrieve an object representing a video scraped and stored in database.
    The hash for each document in the DB is based on the sanitized URL. It serves as an index key
    to check for existant documents and avoid duplicates. When sent on mission, TARS will first see
    if the hash exists in any DB entries. If so, it'll return the matching entry. Otherwise it will
    proceed with scraping and creating a new entry.

    Args:
      args: In order - the URL where TARS should find the video, and the requester (user's id).

    Returns:
      Either a dictionary containing the following attributes related to the video:
      `hash`, `title`, `poster`, `method`, `original_url`, `embed_url`, `duration`;
      or None if the provider does not exist for this video.

    """

    # Store URL, hash and requester's id.
    if forceUrl is None:
      url = args['url']
      self.requester = args['requester']
      hash = args['hash']
      # Save reference in local variable for convenience.
      videostore = self.mongo['collection']

      # Canonize URL (remove any extra attribute on it to avoid duplicates in DB).
      url = self.__canonize_url(url)

      # Check for video in DB: mark task as done in queue if it exists, else trigger a new scrape.
      stored_video = videostore.find_one({ 'hash': hash })

      if stored_video is not None:
        self.__update_queue(self.requester, stored_video, 'ready')
      else:
        self.scrape(url, hash)
    else:
      url = forceUrl
      self.scrape(url, None)

  def scrape(self, url, hash=None):
    """Scrape the URL and create a new entry indexed with the hash passed as argument.

    Args:
      url: A sanitized URL to scrape.
      hash: A md5 hash based on the sanitize URL - serves as index for the document.

    Returns:
      Either dictionary containing the following attributes related to the video:
      hash, title, poster, method, original_url, embed_url, duration.
      Or None if the provider does not exist for this video.

    """

    # From given URL, define provider.
    self.url = url
    self.provider = self.__set_provider(self.url)

    # If not provider is to be found, change status to notfound and stop.
    # Otherwise fetch all needed data by invoking provider's method.
    if self.provider is not None:
      title = self.__get_title()
      poster = self.__get_poster()
      method = self.__get_method()
      original_url = self.__get_original_url()
      embed_url = self.__get_embed_url()
      duration = self.__get_duration()

      video = {}
      if hash:
        video['hash'] = hash
      video['title'] = title
      video['poster'] = poster
      video['method'] = method
      video['original_url'] = original_url
      video['embed_url'] = embed_url
      video['duration'] = duration

      # Store new video in DB, or print dict if a single URL
      # was passed in command line (i.e. we're trying out providers).
      if hash:
        self.__store(video)
      else:
        print(video)
    else:
      if hash:
        self.__update_queue(self.requester, video, 'notfound')
      else:
        print('Provider not found')


  def __set_provider(self, url):
    """Attempt determining the provider based on the given URL.

    Args:
      url: The URL to scrape.

    Returns:
      A provider probe class if a matching one is found, otherwise None.

    """

    # Parse URI and isolate the "authority" part (e.g. "http://www.example.com:80").
    u = urlparse.urlsplit(self.url)
    netloc = u.netloc

    # Remove leading "www".
    if netloc[0:4] == 'www.':
      netloc = netloc[4:]
    netloc = netloc[:netloc.rfind('.')]

    # Invoke factory method to instantiate a provider's probe based on URL.
    provider = factory.create(netloc, url)
    return provider


  def __canonize_url(self, url):
    """Canonize URL by removing extra arguments."""

    # TODO: fix me. Find a better way to sanitize.
    """if '?' in url:
      url = url[:url.rfind('?')]"""

    return url


  def __store(self, video):
    video['created_at'] = datetime.datetime.utcnow()
    collection = self.mongo['collection']

    if collection.find_one({ 'hash': video['hash'] }) is None:
      self.mongo['collection'].insert(video)

    self.__update_queue(self.requester, video, 'ready')


  def __update_queue(self, requester, video, status):
    queue = self.mongo['queue']
    queue.update(
      { 'hash': video['hash'], 'requester': long(requester) },
      { '$set': { 'status': status, 'updated_at': datetime.datetime.utcnow() } }
    )


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
