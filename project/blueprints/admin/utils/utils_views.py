from functools import wraps

def test_decor():
    def decorator(f):
        @wraps(f)
        def decorator_func(*args, **kwargs):
            print('i decorated it')
            return f(*args, **kwargs)
        return decorator_func
    return decorator
