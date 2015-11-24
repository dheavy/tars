# -*- coding: utf-8 -*-
import os
import imp


def create(name, url, logconfig=None):
    """
    Create a new instance of a probe matching the given name.

    Args:
        name: Name of the website - should match with the name of a probe.
        url: URL to scrape - injected into the probe instance upon creation.
        logconfig: Dictionary where keys/values match Logger's configuration.
            Passes logging config down to spawned probe. Defaults to None.

    Returns:
        An instance of the matching probe, if any matches, or None otherwise.

    """
    # Initialize variable class instance we're expecting to return.
    class_inst = None

    # Special case for Facebook. Change name to 'fb' to avoid
    # shadowing the dedicated SDK module of the same name.
    if name == 'facebook':
        name = 'fb'

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
    # with original arguments passed down into it.
    if hasattr(py_module, expected_class):
        class_inst = getattr(py_module, expected_class)(
            url, logconfig=logconfig
        )
    return class_inst
