**Dynamic input-output caching for deterministic functions**

|pypi| |docs| |license|

Features
========

* Keep It Simple, Stupid: A single decorator that does everything for you
* Automagically detects if the decorated function is changed and transparently
  updates cache accordingly without ever returning cached results of the old
  function.

Installation
============

:code:`pip3 install dyncache`

Examples
========

.. code:: python3
   
   # Import the class
   from dyncache import Cache
   # Alternatively you may use the lowercased name
   from dyncache import cache


   # Use with default options. It will create a file "circle_area.dyncache" into
   # the current directory.
   @Cache()
   def circle_area(radius):
       return 3.14159 * (radius ** 2)
       

   # Empty parentheses are not required for the decorator.
   @Cache
   def circle_area(radius):
       return 3.14159 * (radius ** 2)


   circle_area(2)  # Calculates and returns
   circle_area(3)  # Calculates and returns
   circle_area(2)  # Returns from cache


   # Saves the cache to /tmp/hello.world.
   @Cache(root="/tmp", filename="hello.world")
   def circle_area(radius):
       ...


   # Use for function with large input/output -values.
   @Cache(largeitems=True)
   def load_all_api_data_for_a_day(day):
       ...


   # When items are small and cache would update too often, setting autowrite to
   # False lets you control when the cached data is written to the file.
   cache = Cache(autowrite=False)
   @cache
   def really_frequent_function(a, b):
       ...
   ...
   cache.write()  # Write cache data to the file
   sys.exit(0)


Contributing
============

* Send any issues to GitHub's issue tracker.
* Before sending a pull request, format it with `Black`_ (-Sl79)
* Any changes must be updated to the documentation
* All pull requests must be tested with tox (if you are using pyenv, add the installed versions for py35-py38 and pypy3 to .python-version at the root of this repository before running tox)


.. _`Black`: https://github.com/psf/black

.. |pypi| image:: https://img.shields.io/pypi/v/dyncache.svg
    :alt: PyPI
    :target: https://pypi.org/project/dyncache/
.. |docs| image:: https://readthedocs.org/projects/dyncache/badge/?version=latest
    :alt: Read the Docs
    :target: http://dyncache.readthedocs.io/en/latest/
.. |license| image:: https://img.shields.io/github/license/b10011/dyncache.svg
    :alt: License
    :target: https://github.com/b10011/dyncache/blob/master/LICENSE
