import imp
import os


def create(name, url):
  """Create a new instance of a probe matching the given name.

  Args:
    name: The name of the website — should be matching with the name of a probe.
    url: The URL to scrape — will be injected to the probe instance upon creation.

  Returns:
    An instance of the matching probe, if any matches, or None otherwise.

  """
  class_int = None
  expected_class = name.capitalize()
  filepath = os.path.dirname(os.path.realpath(__file__)) + '/probes/' + name + '.py'

  mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

  try:
    py_mod = imp.load_source(mod_name, filepath)
  except FileNotFoundError:
    return None

  if hasattr(py_mod, expected_class):
    class_inst = getattr(py_mod, expected_class)(url)

  return class_inst
