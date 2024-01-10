import os.path
import sys
from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        namespace = sys._getframe(1).f_globals  # caller's globals
        function_path = os.path.dirname(namespace['__file__']).split(os.path.sep)[-1]
        args_line = []
        if len(args) > 0:
            args = map(str, args)
            args_line.append(f"{', '.join(args)}")
        if len(kwargs) > 0:
            args_line.append(f"{', '.join([f'{key}={value}' for key, value in kwargs.items()])}")
        if func.__globals__['__package__'] is not None and len(func.__globals__['__package__']) > 0:
            function_path = func.__globals__['__package__']

        print(f'Function {function_path}::{func.__name__}({", ".join(args_line)}) Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper
