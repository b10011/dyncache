import cloudpickle
from types import FunctionType, MethodType
from pathlib import Path
import click
import inspect
import struct
from .functionhash import get_function_hash


class FunctionHashMismatch(Exception):
    """
    Internal exception that is raised when function has changed and the cache
    should be invalidated.
    """

    pass


class Cache:
    """
    Dynamic input-output caching for deterministic functions.

    :param root:
        A folder in which to save the cache file.
    :type root: str or None

    :param filename:
        File name for the cache, the default is "<function_name>.dyncache"
    :type filename: str or None

    :param largeitems:
        In case the function takes in or returns large values, this should be
        toggled on or cache reading/writing performance will suffer.
    :type largeitems: bool

    :param autowrite:
        Whether or not the cache should automatically be written on new items.
        Alternatively there is cacheinstance.write() for manual writing.
    :type autowrite: bool
    """

    def __init__(self, *args, **kwargs):
        self.root = None
        self.filename = None
        self.largeitems = False
        self.logs = True
        self.autowrite = True

        self.function = None
        self.functionhash = None
        self.cachedfunctionhash = None
        self.cachedict = None
        self.cachepath = None

        # Constants
        self._signatures = [
            (self._functionwrapper, inspect.signature(self._functionwrapper)),
            (self._decorator, inspect.signature(self._decorator)),
        ]

        # Parse given arguments
        self(*args, **kwargs)

    # READ AND WRITE
    def read(self):
        """
        Read the cache file.
        """

        if not self.cachepath.exists():
            raise FileNotFoundError("Cache doesn't exists")

        elif self.cachepath.is_dir():
            raise IsADirectoryError("Cache is not a file")

        else:
            with self.cachepath.open("rb") as f:
                largeitems = cloudpickle.load(f)
                cachedfunctionhash = cloudpickle.load(f)
                (itemcount,) = struct.unpack("<I", f.read(4))
                if cachedfunctionhash != self.functionhash:
                    raise FunctionHashMismatch("Function has changed")

                self.largeitems = largeitems
                self.cachedfunctionhash = cachedfunctionhash

                if self.largeitems:
                    self.cachedict = dict()
                    with click.progressbar(
                        length=itemcount, show_pos=True
                    ) as bar:
                        for _ in range(itemcount):
                            key, value = cloudpickle.load(f)
                            self.cachedict[key] = value
                            bar.update(1)

                else:
                    self.cachedict = cloudpickle.load(f)

    def write(self):
        """
        Write the cache file.
        """

        with self.cachepath.open("wb") as f:
            cloudpickle.dump(self.largeitems, f)
            cloudpickle.dump(self.functionhash, f)
            f.write(struct.pack("<I", len(self.cachedict)))
            if self.largeitems:
                with click.progressbar(
                    self.cachedict.items(), show_pos=True
                ) as bar:
                    for pair in bar:
                        cloudpickle.dump(pair, f)
            else:
                cloudpickle.dump(self.cachedict, f)

    # CACHING FUNCTIONS

    def _cache_or_eval(self, *args, **kwargs):

        # Cache is not yet loaded
        if self.cachedict is None or self.cachedfunctionhash is None:
            try:
                self.read()
            except (
                FileNotFoundError,
                IsADirectoryError,
                FunctionHashMismatch,
            ):
                # Create new cache
                self.cachedict = dict()
                self.cachedfunctionhash = self.functionhash

        frozenkwargs = frozenset(kwargs.items())
        key = (args, frozenkwargs)
        try:
            return self.cachedict[key]
        except KeyError:
            value = self._call_function(*args, **kwargs)
            self.cachedict[key] = value
            if self.autowrite:
                self.write()
            return value

    def _call_function(self, *args, **kwargs):
        if not self.function:
            raise ValueError("Function has not been provided yet")
        return self.function(*args, **kwargs)

    # DECORATOR PARSER FUNCTIONS
    def __call__(self, *args, **kwargs):
        if self.function is None:
            self._parse_args(*args, **kwargs)
            return self
        else:
            return self._cache_or_eval(*args, **kwargs)

    def _decorator(
        self,
        root=None,
        filename=None,
        largeitems=False,
        logs=True,
        autowrite=False,
    ):
        self.root = root
        self.filename = filename
        self.largeitems = largeitems
        self.logs = logs
        self.autowrite = autowrite

    def _functionwrapper(self, function):
        if not isinstance(function, (FunctionType, MethodType)):
            raise TypeError()

        self.function = function
        self.functionhash = get_function_hash(self.function)

        if self.root is not None:
            self.cachepath = Path(self.root)
        else:
            self.cachepath = Path()

        if self.filename is not None:
            self.cachepath = self.cachepath / self.filename
        else:
            self.cachepath = self.cachepath / "{}.dyncache".format(
                self.function.__name__
            )

    def _parse_args(self, *args, **kwargs):
        for parser_func, signature in self._signatures:
            try:
                signature.bind(*args, **kwargs)
                parser_func(*args, **kwargs)
                break
            except TypeError:
                continue
        else:
            raise ValueError("Invalid arguments")
