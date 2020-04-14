from hashlib import sha256
import cloudpickle
from .version import PYTHON_VERSION


def get_function_hash_py35_to_py37(function):
    code = function.__code__
    return sha256(
        cloudpickle.dumps(
            (
                code.co_argcount,
                code.co_cellvars,
                code.co_code,
                code.co_consts,
                code.co_flags,
                code.co_freevars,
                code.co_kwonlyargcount,
                code.co_lnotab,
                code.co_name,
                code.co_names,
                code.co_nlocals,
                code.co_stacksize,
                code.co_varnames,
            )
        )
    ).digest()


def get_function_hash_python38_to_latest(function):
    code = function.__code__

    return sha256(
        cloudpickle.dumps(
            (
                code.co_argcount,
                code.co_cellvars,
                code.co_code,
                code.co_consts,
                code.co_flags,
                code.co_freevars,
                code.co_kwonlyargcount,
                code.co_lnotab,
                code.co_name,
                code.co_names,
                code.co_nlocals,
                code.co_posonlyargcount,
                code.co_stacksize,
                code.co_varnames,
            )
        )
    ).digest()


if PYTHON_VERSION >= (3, 8):
    get_function_hash = get_function_hash_python38_to_latest
elif PYTHON_VERSION >= (3, 5):
    get_function_hash = get_function_hash_py35_to_py37
else:
    raise Exception("Python version not supported")
