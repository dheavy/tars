# -*- coding: utf-8 -*-


import os
import imp


def create(name, url):
    """
    Create a new instance of a probe matching the given name.

    Args:
        name: Name of the website - should match with the name of a probe.
        url: URL to scrape - injected into the probe instance upon creation.

    Returns:
        An instance of the matching probe, if any matches, or None otherwise.

    """
    # Initialize variable class instance we're expecting to return.
    class_inst = None

    # Capitalize the name passed as argument to (hopefully)
    # obtain the name of the class we're expecting to instantiate,
    # and build the file path to its file.
    expected_class = name.capitalize()
    filepath = (os.path.dirname(os.path.realpath(__file__)) +
                '/' + name + '.py')

    # Unpack module name into a variable.
    mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])

    # Artifically load module and reference it in a variable.
    try:
        py_module = imp.load_source(mod_name, filepath)
    except EnvironmentError:
        return None

    # If loaded module has expected class, artifically load a class instance
    # with expected `url` argument in it.
    if hasattr(py_module, expected_class):
        class_inst = getattr(py_module, expected_class)(url)

    return class_inst
