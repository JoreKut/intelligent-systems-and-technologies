import functools


def on_exception(exc_types: list[type], return_value: object):
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):

            try:
                return fn(*args, **kwargs)
            except (*exc_types, ):
                print("return default value=", return_value)
                return return_value

        return inner

    return wrapper
