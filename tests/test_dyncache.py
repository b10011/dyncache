from dyncache import cache, Cache, FunctionHashMismatch
from pathlib import Path
import pytest


def test_function_without_args():
    cachepath = Path("f1.dyncache")
    if cachepath.exists():
        cachepath.unlink()

    @Cache
    def f1(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f1(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f1(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f1(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_function_with_empty_args():
    cachepath = Path("f2.dyncache")
    if cachepath.exists():
        cachepath.unlink()

    cache = Cache()

    @cache
    def f2(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f2(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f2(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f2(1, 2) == 0.5
    assert globals()["__cached__"]

    assert not cachepath.exists()

    cache.write()

    assert cachepath.exists()

    if cachepath.exists():
        cachepath.unlink()


def test_function_with_unnamed_args():
    cachepath = Path("/tmp/f3.dyncache")
    if cachepath.exists():
        cachepath.unlink()

    @Cache("/tmp")
    def f3(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f3(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f3(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f3(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_function_with_named_args():
    cachepath = Path("/tmp/f4.dyncache")
    if cachepath.exists():
        cachepath.unlink()

    cache = Cache(root="/tmp")

    @cache
    def f4(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f4(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f4(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f4(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_cache_is_a_folder():
    cachepath = Path("/tmp/f5.dyncache")
    if cachepath.exists():
        cachepath.rmdir()

    cachepath.mkdir(parents=True)

    cache = Cache(root="/tmp")

    @cache
    def f5(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f5(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f5(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f5(1, 2) == 0.5
    assert globals()["__cached__"]

    cachepath.rmdir()

    if cachepath.exists():
        cachepath.unlink()


def test_largeitems():
    cachepath = Path("f6.dyncache")
    if cachepath.exists():
        cachepath.unlink()

    cache = Cache(largeitems=True)

    @cache
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    cache.write()

    if cachepath.exists():
        cachepath.unlink()


def test_with_filename():
    cachepath = Path("hello.world")
    if cachepath.exists():
        cachepath.unlink()

    cache = Cache(filename="hello.world")

    @cache
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_with_multiple_functions():
    cache = Cache(largeitems=True)

    @cache
    def f1(func):
        return func() + 1

    def f2():
        return 2

    assert f1(f2) == 3


def test_invalid_arguments():
    with pytest.raises(ValueError):
        Cache(hello="world")


def test_undefined_function():
    cache = Cache()
    with pytest.raises(ValueError):
        cache._call_function(hello="world")


def test_autowrite():
    cachepath = Path("hello.world")
    if cachepath.exists():
        cachepath.unlink()

    cache = Cache(filename="hello.world", autowrite=True)

    assert not cachepath.exists()

    @cache
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    assert not cachepath.exists()

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    assert cachepath.exists()

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    assert cachepath.exists()

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    assert cachepath.exists()

    if cachepath.exists():
        cachepath.unlink()


def test_cachereading():
    cachepath = Path("readthis.cache")
    if cachepath.exists():
        cachepath.unlink()

    tmp = Cache(filename="readthis.cache", autowrite=True)

    @tmp
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    cache = Cache(filename="readthis.cache")

    @cache
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_cachereading_changed_function_name():
    cachepath = Path("readthis2.cache")
    if cachepath.exists():
        cachepath.unlink()

    tmp = Cache(filename="readthis2.cache", autowrite=True)

    @tmp
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    cache = Cache(filename="readthis2.cache")

    @cache
    def NEWNAME(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_cachereading_largeitems():
    cachepath = Path("readthis4.cache")
    if cachepath.exists():
        cachepath.unlink()

    tmp = Cache(filename="readthis4.cache", autowrite=True, largeitems=True)

    @tmp
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    cache = Cache(filename="readthis4.cache")

    @cache
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_functionchange():
    cachepath = Path("changefunction.cache")
    if cachepath.exists():
        cachepath.unlink()

    tmp = Cache(filename="changefunction.cache", autowrite=True)

    @tmp
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 0.5
    assert globals()["__cached__"]

    cache = Cache(filename="changefunction.cache")

    @cache
    def f6(a, b):
        globals()["__cached__"] = False
        return a * a * b

    globals()["__cached__"] = True
    assert f6(1, 2) == 2
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 1) == 1
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert f6(1, 2) == 2
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()


def test_lowercased_decorator():
    cachepath = Path("lowercased.dyncache")
    if cachepath.exists():
        cachepath.unlink()

    @cache
    def lowercased(a, b):
        globals()["__cached__"] = False
        return a * a / b

    globals()["__cached__"] = True
    assert lowercased(1, 2) == 0.5
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert lowercased(1, 1) == 1.0
    assert not globals()["__cached__"]

    globals()["__cached__"] = True
    assert lowercased(1, 2) == 0.5
    assert globals()["__cached__"]

    if cachepath.exists():
        cachepath.unlink()
