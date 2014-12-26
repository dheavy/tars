import urllib
import datetime
import requests
import bs4
from mypleasure.utils.timer import Timer
from mypleasure.providers import factory


class Tars:

  def __init__(self):

    self.url = None
    self.provider = None
    self.markups = []

    print("\n*")
    print("*  TARS, on duty [" + str(datetime.datetime.now()) + "]")
    print("*  //////////////////////////////////////////")

  def send_on_mission(self, url):
    self.url = self.__sanitize_url(url)
    self.provider = self.__set_provider(self.url)

    if self.provider == None:
      print("*    - no probe found: aborting mission.")
      print("*\n")
      return
    else:
      print("*    - found matching probe: " + self.provider.name)

    id = self.__get_id()
    print("*    - id: " + id)

    title = self.__get_title()
    print("*    - title: " + title)

    poster = self.__get_poster()
    print("*    - poster: " + poster)

    method = self.__get_method()
    print("*    - method: " + method)

    original_url = self.__get_original_url()
    print("*    - original url: " + original_url)

    embed_url = self.__get_embed_url()
    print("*    - embed url: " + embed_url)

    duration = self.__get_duration()
    print("*    - duration: " + duration)
    print("*")

    video = {}
    video['id'] = id
    video['title'] = title
    video['poster'] = poster
    video['method'] = method
    video['original_url'] = original_url
    video['embed_url'] = embed_url

    return video

  def __set_provider(self, url):
    u = urllib.parse.urlsplit(self.url)
    netloc = u.netloc

    if netloc[0:4] == 'www.':
      netloc = netloc[4:]
    netloc = netloc[:netloc.rfind('.')]

    print("*")
    print("*  Determining Provider (fetching probe \"" + netloc + "\")")

    provider = factory.create(netloc, url)
    return provider

  def __sanitize_url(self, url):
    print("*")
    print("*  Sanitizing URL")
    print("*    - was " + url)

    url = url[:url.rfind('?')]

    print("*    - now " + url)
    return url

  def __get_id(self):
    return self.provider.get_id()

  def __get_title(self):
    return self.provider.get_title()

  def __get_poster(self):
    return self.provider.get_poster()

  def __get_method(self):
    return self.provider.get_method()

  def __get_original_url(self):
    return self.provider.get_original_url()

  def __get_embed_url(self):
    return self.provider.get_embed_url()

  def __get_duration(self):
    return self.provider.get_duration()
