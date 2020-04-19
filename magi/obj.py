from numbers import Number

def is_integer(o):
    return isinstance(o, (int, long))

def is_number(o):
    return isinstance(o, Number)

def is_iterable(o):
    try:
        _ = iter(o)
        return True
    except TypeError:
        return False

def is_string(o):
    return isinstance(o, (str, unicode))

def is_coll(o):
    return not is_string(o) and is_iterable(o)

