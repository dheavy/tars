import imp
import os


def create(name, url):
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
