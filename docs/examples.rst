Examples
========

.. code:: python3
   
   # Import the class
   from dyncache import Cache


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
