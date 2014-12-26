class BaseProbe:

  name = "BaseProbe"

  def __init__(self, url):
    self.data = {
      'id': None,
      'title': None,
      'poster': None,
      'method': None,
      'original_url': url,
      'embed_url': None,
      'duration': None
    }
    self.url = url
    self.process()

  def process(self):
    pass

  def get_id(self):
    return self.data['id']

  def get_title(self):
    return self.data['title']

  def get_poster(self):
    return self.data['poster']

  def get_method(self):
    return self.data['method']

  def get_original_url(self):
    return self.data['original_url']

  def get_embed_url(self):
    return self.data['embed_url']

  def get_duration(self):
    return self.data['duration']

  def __extract_id(self):
    pass

  def __scrape_title(self, markup):
    pass

  def __scrape_poster(self, markup):
    pass

  def __scrape_embed_url(self, markup):
    pass

  def __scrape_duration(self, markup):
    pass
